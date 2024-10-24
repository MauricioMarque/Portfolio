--select * from Sales.SalesOrderHeader 
--select * from Sales.SalesOrderDetail
--select * from Production.Product
--select * from Person.Address
--select * from Person.StateProvince

SELECT

	h.OrderDate AS "Data do Pedido", 
	h.TotalDue AS "Valor Total", 
	h.ShipToAddressID,
	pr.StateProvinceID AS "Regiao",
	p.Name AS "Produto"
	
FROM Sales.SalesOrderHeader AS h 

	INNER JOIN Sales.SalesOrderDetail AS d 

		ON h.SalesOrderID = d.SalesOrderID

	INNER JOIN Production.Product AS p

		ON d.ProductID = p.ProductID

	INNER JOIN Person.StateProvince AS pr

		ON pr.TerritoryID = h.TerritoryID
