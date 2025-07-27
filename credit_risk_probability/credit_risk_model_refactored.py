import os
import pandas as pd
import gc
import lightgbm as lgb
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import (
    roc_auc_score, accuracy_score, f1_score,
    precision_score, recall_score, confusion_matrix, 
    ConfusionMatrixDisplay, classification_report, roc_curve, 
    precision_recall_curve
)
from scipy.stats import randint, uniform
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Optional

class CreditRiskDataProcessor:
    """Class to handle data loading, processing, and merging for credit risk modeling."""
    
    def __init__(self, base_path: str, case_id_threshold: int = 100000):
        self.base_path = base_path
        self.case_id_threshold = case_id_threshold
        self.df_merge = None
        self.df_merge_test = None
        
    def load_and_filter_base(self, data_type: str) -> pd.DataFrame:
        """Load and filter base parquet file."""
        file_path = os.path.join(self.base_path, data_type, f"{data_type}_base.parquet")
        df = pd.read_parquet(file_path, engine='pyarrow')
        return df[df['case_id'] <= self.case_id_threshold]
    
    def load_and_filter_files(self, prefix: str, data_type: str) -> pd.DataFrame:
        """Load and filter parquet files with given prefix."""
        pasta = os.path.join(self.base_path, data_type)
        arquivos = [
            os.path.join(pasta, f) for f in os.listdir(pasta)
            if f.startswith(f"{data_type}_{prefix}_") and f.endswith(".parquet")
        ]
        
        dataframes_filtrados = []
        for arquivo in arquivos:
            df_case_id = pd.read_parquet(arquivo, columns=['case_id'], engine='pyarrow')
            
            if prefix == "credit_bureau" and (df_case_id['case_id'].min() > self.case_id_threshold or df_case_id['case_id'].max() < 0):
                continue
                
            if df_case_id['case_id'].max() < 1000:
                df_temp = df_case_id[df_case_id['case_id'] <= self.case_id_threshold]
            else:
                df_temp = pd.read_parquet(arquivo, engine='pyarrow')
                df_temp = df_temp[df_temp['case_id'] <= self.case_id_threshold]
                
            if not df_temp.empty:
                df_temp['case_id'] = df_temp['case_id'].astype('int32')
                dataframes_filtrados.append(df_temp)
                
            del df_case_id, df_temp
            gc.collect()
            
        df_concat = pd.concat(dataframes_filtrados, ignore_index=True)
        print(f"Arquivos {prefix} processados: {len(arquivos)}")
        print(f"Total de linhas após filtro: {len(df_concat)}")
        return df_concat.drop_duplicates(subset='case_id', keep='first')
    
    def load_single_file(self, file_name: str, data_type: str) -> pd.DataFrame:
        """Load and filter a single parquet file."""
        file_path = os.path.join(self.base_path, data_type, f"{data_type}_{file_name}.parquet")
        df = pd.read_parquet(file_path, engine='pyarrow')
        df = df[df['case_id'] <= self.case_id_threshold]
        return df.drop_duplicates(subset='case_id', keep='first')
    
    @staticmethod
    def clean_object_columns(df: pd.DataFrame) -> pd.DataFrame:
        """Remove object columns ending with 'D' and convert 'M', 'L', 'T' to category."""
        object_columns = df.select_dtypes(include='object').columns
        for col in object_columns:
            if col.endswith('D'):
                df.drop(columns=[col], inplace=True)
            elif col.endswith(('M', 'L', 'T')):
                df[col] = df[col].astype('category')
        return df
    
    @staticmethod
    def unify_merge_columns(df: pd.DataFrame) -> pd.DataFrame:
        """Unify columns with _x and _y suffixes."""
        cols_x = [col for col in df.columns if col.endswith('_x')]
        for col_x in cols_x:
            base_col = col_x[:-2]
            col_y = base_col + '_y'
            if col_y in df.columns:
                df[base_col] = df[col_x].combine_first(df[col_y])
                df.drop(columns=[col_x, col_y], inplace=True)
            else:
                df.rename(columns={col_x: base_col}, inplace=True)
        return df
    
    def process_dataset(self, data_type: str) -> pd.DataFrame:
        """Process and merge all datasets for train or test."""
        df_base = self.load_and_filter_base(data_type)
        df_merge = df_base.copy()
        
        datasets = [
            ('applprev', self.load_and_filter_files, 'applprev'),
            ('credit_bureau', self.load_and_filter_files, 'credit_bureau'),
            ('deposit', self.load_single_file, 'deposit_1'),
            ('other', self.load_single_file, 'other_1'),
            ('person', self.load_and_filter_files, 'person'),
            ('static', self.load_and_filter_files, 'static'),
            ('tax', self.load_and_filter_files, 'tax_registry')
        ]
        
        for name, load_func, prefix in datasets:
            df_temp = load_func(prefix, data_type)
            df_merge = pd.merge(df_merge, df_temp, how='outer', on='case_id')
            df_merge = self.unify_merge_columns(df_merge)
            df_merge = self.clean_object_columns(df_merge)
            if data_type == 'train':
                df_merge = df_merge.drop(columns=['MONTH', 'WEEK_NUM', 'date_decision'], errors='ignore')
        
        return df_merge
    
    def align_columns(self, df_train: pd.DataFrame, df_test: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
        """Align columns between train and test datasets."""
        for col in df_train.columns:
            if col != 'target' and col not in df_test.columns:
                df_train.drop(columns=[col], inplace=True)
        for col in df_test.columns:
            if col != 'target' and col not in df_train.columns:
                df_test.drop(columns=[col], inplace=True)
        return df_train, df_test
    
    def train_model(self, X_train: pd.DataFrame, y_train: pd.Series) -> lgb.LGBMClassifier:
        """Train LightGBM model with hyperparameter tuning."""
        model = lgb.LGBMClassifier(objective='binary', boosting_type='gbdt', random_state=42)
        param_dist = {
            'num_leaves': randint(20, 150),
            'max_depth': randint(3, 15),
            'learning_rate': uniform(0.01, 0.1),
            'n_estimators': randint(50, 500)
        }
        
        random_search = RandomizedSearchCV(
            model,
            param_distributions=param_dist,
            scoring='roc_auc',
            n_iter=30,
            cv=3,
            random_state=42,
            n_jobs=-1,
            verbose=1
        )
        
        print("Iniciando busca por melhores hiperparâmetros...")
        random_search.fit(X_train, y_train)
        print("Busca finalizada.")
        
        print("Melhores parâmetros encontrados:", random_search.best_params_)
        best_model = lgb.LGBMClassifier(
            objective='binary',
            boosting_type='gbdt',
            random_state=42,
            **random_search.best_params_
        )
        best_model.fit(X_train, y_train)
        return best_model
    
    def evaluate_model(self, model: lgb.LGBMClassifier, X_train: pd.DataFrame, y_train: pd.Series):
        """Evaluate model performance on training data."""
        y_pred = model.predict(X_train)
        y_pred_proba = model.predict_proba(X_train)[:, 1]
        
        print("\n📊 Métricas no conjunto de treino:")
        print(f"AUC: {roc_auc_score(y_train, y_pred_proba):.4f}")
        print(f"Accuracy: {accuracy_score(y_train, y_pred):.4f}")
        print(f"F1-score: {f1_score(y_train, y_pred):.4f}")
        print(f"Precision: {precision_score(y_train, y_pred):.4f}")
        print(f"Recall: {recall_score(y_train, y_pred):.4f}")
        print("\nRelatório de Classificação:")
        print(classification_report(y_train, y_pred))
        
        # Matriz de confusão
        cm = confusion_matrix(y_train, y_pred)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm)
        disp.plot()
        plt.title("Matriz de Confusão - Treino")
        plt.show()
        
        # Curva ROC
        fpr, tpr, _ = roc_curve(y_train, y_pred_proba)
        plt.plot(fpr, tpr, label='ROC Curve')
        plt.plot([0, 1], [0, 1], linestyle='--', label='Random')
        plt.xlabel('FPR (Falsos Positivos)')
        plt.ylabel('TPR (Verdadeiros Positivos)')
        plt.title('Curva ROC - Treino')
        plt.legend()
        plt.grid()
        plt.show()
        
        # Curva Precisão-Recall
        precision, recall, _ = precision_recall_curve(y_train, y_pred_proba)
        plt.plot(recall, precision, label='Precision-Recall Curve')
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.title('Curva Precisão vs. Recall - Treino')
        plt.grid()
        plt.show()
        
        # Distribuição dos scores
        plt.figure(figsize=(8, 4))
        sns.histplot(y_pred_proba, bins=50, kde=True)
        plt.title('Distribuição dos Scores (Probabilidades) - Treino')
        plt.xlabel('Score')
        plt.ylabel('Frequência')
        plt.show()
        
    def predict_and_save(self, model: lgb.LGBMClassifier, X_test: pd.DataFrame, case_id_test: pd.Series):
        """Generate predictions and save to CSV."""
        y_pred_proba = model.predict_proba(X_test)[:, 1]
        df_scores = pd.DataFrame({
            'case_id': case_id_test,
            'score': y_pred_proba
        })
        df_scores.to_csv('scores_case_id.csv', index=False)
        print("Arquivo 'scores_case_id.csv' salvo com sucesso.")
        
        # Plot feature importance
        lgb.plot_importance(model, max_num_features=20, importance_type='gain')
        plt.title('Importância das Variáveis')
        plt.show()
    
    def run_pipeline(self):
        """Run the complete data processing and modeling pipeline."""
        # Process train and test datasets
        self.df_merge = self.process_dataset('train')
        self.df_merge_test = self.process_dataset('test')
        
        # Align columns
        self.df_merge, self.df_merge_test = self.align_columns(self.df_merge, self.df_merge_test)
        
        # Prepare data for modeling
        X_train = self.df_merge.drop(columns=['case_id', 'target'])
        y_train = self.df_merge['target']
        X_test = self.df_merge_test.drop(columns=['case_id'])
        case_id_test = self.df_merge_test['case_id']
        
        # Train model
        model = self.train_model(X_train, y_train)
        
        # Evaluate model
        self.evaluate_model(model, X_train, y_train)
        
        # Predict and save results
        self.predict_and_save(model, X_test, case_id_test)

if __name__ == "__main__":
    base_path = r"C:\Users\mau_a\OneDrive\Área de Trabalho\home-credit-credit-risk-model-stability\parquet_files"
    processor = CreditRiskDataProcessor(base_path)
    processor.run_pipeline()