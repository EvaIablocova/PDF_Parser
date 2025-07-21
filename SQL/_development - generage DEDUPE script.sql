USE PDFparser
GO

DECLARE @SQL NVARCHAR(4000) = '
-------------------------------------------------------------------------
IF @TableName IN( ''ALL'',''#tableName#'')
BEGIN
	;WITH DedupeRecords AS (
		SELECT *
			,RN = ROW_NUMBER() OVER (Partition By #columns# ORDER BY [Id] Desc)
		FROM #TableName#
		)
	DELETE FROM DedupeRecords
	WHERE RN > 1

	PRINT ''Cleaned table:[#tableName#]''
END
'

--Select top 100 *
; WITH AggregatedColumns AS (
		SELECT TABLE_NAME, _Columns = STRING_AGG(CONCAT('[',COLUMN_NAME,']'),',') WITHIN GROUP ( ORDER BY Ordinal_Position)
		from INFORMATION_SCHEMA.COLUMNS
		WHERE 1=1
		AND TABLE_NAME like 'Staging%'
		AND COLUMN_NAME NOT IN ('ID')
		Group By TABLE_NAME
		)
SELECT _SQL = REPLACE(REPLACE(@SQL,'#TableName#',TABLE_NAME),'#columns#',_Columns)
FROM AggregatedColumns