# Etapas

- Carregamento dos dados com pandas

- O arquivos dados.json não conseguir ser aberto em função da diferença de comprimentos de arrays, então abri utilizando a bilbioteca json.

- A partir de pesquisa sobre como o cpf é considerado válido, utilizei um script para validação do cpf, e ao final retornando se o cpf é válido ou inválido.

- O nome completo apenas validei de forma manual, através da leitura do nome presente no arquivo json, e dei um veredito a respeito do seu nome estar completo ou não.

- Para a idade, utilizei da bilbioteca datetime para uso da data de hoje e conversão da data de nascimento presente no dataset para formato date, a partir dai conseguir criar uma função para realizar a diferença destes pontos e garantir a idade correta do cliente.

- Da mesma forma que o nome fiz a validação do email de forma manual, ao conferir os emails presentes no sistema, verifiquei que todos são corporativos ou de instituições de ensino, e o email do cliente parece ser pessoas então considerei-o inválido.

- Checando o telefone, utilizei de um script para validação do telefone e retorno em texto respondendo se é ou não um telefone válido.

- Para checagem do CEP utilizei do url em questão sugerido e utilizei de um script para agora com inputação de cep verificar a validade do cep e retornar os parâmetros de endereço relativos ao cep em questão.

- Após todo o processo, utilizei do método inner join na coluna de cpf para verificar quais clientes estavam presentes no sistema e quais não.

- Acabei encontrando apenas um cliente em nossos dados que já estava presente no sistema.

- Utilizando o método isin consegui separar os clientes que estavam já no sistema dos que não estavam, e salvei os que não estavam em JSON e os que estavam em xlsx, para futura inputação.

#### Valeu!!!
