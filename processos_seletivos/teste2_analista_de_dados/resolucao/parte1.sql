

-- 1 Qual designer de jogos possui a maior m�dia de avalia��o dentre todos os seus jogos publicados? Atente-se a qual tipo de media � a mais adequada aos dados fornecidos.

select top 1 d.designer, avg(r.avg_rating) as average_rating 
	from dbo.Designer_category d 
	inner join dbo.Rating r 
	on d.game_id = r.game_id 
	group by d.designer 
	order by avg(r.avg_rating) desc




-- 2 Quais os 5 jogos com durabilidade de at� 120 min pior avaliados? E quais os melhores?

-- Piores avaliados

select top 5 b.game_id, b.names, r.avg_rating
	from dbo.Board_game_principal b 
	inner join dbo.Rating r 
	on b.game_id = r.game_id 
	where b.max_time <= 120 
	order by r.avg_rating asc

-- Melhores avaliados

select top 5 b.game_id, b.names, r.avg_rating
	from dbo.Board_game_principal b 
	inner join dbo.Rating r 
	on b.game_id = r.game_id 
	where b.max_time <= 120 
	order by r.avg_rating desc




-- 3 Um cliente pretende comprar os 5 jogos melhor avaliados que atendam �s seguintes caracter�sticas: seja da categoria fic��o cient�fica (�Science Fiction�), o m�ximo de jogadores seja 6 e possua a mec�nica de controle de �rea (�Area control�) . 
-- Quais jogos o cliente deve p�r no carrinho?

select top 5 b.game_id, b.names, r.avg_rating, d.category, b.max_players, b.mechanic
	from dbo.Board_game_principal b 
	inner join dbo.Rating r 
	on b.game_id = r.game_id 
	inner join  dbo.Designer_category d
	on d.game_id = b.game_id
	where d.category like '%Science Fiction%'
	and b.max_players <= 6
	and b.mechanic like '%Area Control%'
	order by r.avg_rating desc

