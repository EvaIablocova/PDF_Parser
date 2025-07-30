USE [PDFparser]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
/*===================================================================================================================
 Stored Procedure  : dbo.Export_Delta_To_CSV

 Purpose      : Export Delta to CSV files
 Input Parameters  : @File_name

 Output Parameters  : returns 0 if no rows are exported
					  returns 1 if export SQL was performed

 Usage        : EXEC [PDFparser].dbo.Export_Delta_To_CSV 'Lichidarea'

=====================================================================================================================*/
CREATE OR ALTER PROCEDURE [dbo].[Export_Delta_To_CSV]
  @File_name NVARCHAR(128)
--WITH EXECUTE AS 'NewUser2'
AS
BEGIN
  SET NOCOUNT ON;

  --DECLARE @File_name NVARCHAR(260)
  --SET @File_name = 'Denumirea'

  DECLARE 
    @Date_last_exported DATE,
    @Today DATE = GETDATE(),
    @RowCount INT,
    @bcpCommand NVARCHAR(4000),
    @ExportFile NVARCHAR(260),
	@sql NVARCHAR(MAX);


  --SET @ExportFile = N'C:\Users\evaia\PycharmProjects\PDF_Parser3\Export\' + @File_name + '_' + CONVERT(NVARCHAR(8), @Today, 112) + '.csv';
  SET @ExportFile = N'C:\Export\' + @File_name + '_' + CONVERT(NVARCHAR(8), @Today, 112) + '.csv';
  print @ExportFile

  -- Get last inserted date
  SELECT @Date_last_exported = Date_last_exported
  FROM [PDFparser].[dbo].[ETL_controll]
  WHERE File_name = @File_name;

  PRINT 'Date_last_exported: ' + CONVERT(NVARCHAR(10), @Date_last_exported, 120);
  PRINT 'Today: ' + CONVERT(NVARCHAR(30), @Today, 120);

  -- If last inserted date is today, do nothing
  IF @Date_last_exported = @Today
    RETURN 0;

  -- Check if there are rows to export SQL
	SET @sql = N'
	  SELECT @RowCount_OUT = COUNT(*)
	  FROM [PDFparser].[dbo].[' + @File_name + N']
	  WHERE [DateCreated] > @Date_last_exported
	';
	
	PRINT @sql

	EXEC sp_executesql
	  @sql,
	  N'@Date_last_exported DATE, @RowCount_OUT INT OUTPUT',
	  @Date_last_exported = @Date_last_exported,
	  @RowCount_OUT = @RowCount OUTPUT;

	  PRINT 'RowCount: ' + CAST(@RowCount AS NVARCHAR(10));

  IF @RowCount = 0
    RETURN 0;

 
  IF OBJECT_ID('exported_data', 'U') IS NOT NULL
    DROP TABLE exported_data;

	SET @sql = N'SELECT * INTO exported_data FROM [PDFparser].[dbo].[' + @File_name + N']
	WHERE [DateCreated] > @Date_last_exported';

	EXEC sp_executesql @sql, N'@Date_last_exported DATETIME', @Date_last_exported = @Date_last_exported;

	DECLARE @cols NVARCHAR(MAX), @sqlColumns NVARCHAR(MAX);

	SELECT @cols = STRING_AGG('CHAR(34) + CAST(' + QUOTENAME(name) + ' AS NVARCHAR(MAX)) + CHAR(34)', ' + '','' + ')
	FROM sys.columns
	WHERE object_id = OBJECT_ID('[dbo].[exported_data]');

	--IF @cols IS NULL
 --   PRINT 'No columns found or table does not exist.';

	print @cols

	SET @sqlColumns = 'SELECT ' + @cols + ' FROM [PDFparser].[dbo].[exported_data]';

	print @sqlColumns

	SET @bcpCommand =
		N'bcp "' + @sqlColumns + '" queryout "' + @ExportFile +
		N'" -c -t"" -U NewUser2 -P MyStr0ngPass123 -S localhost';

	print @bcpCommand
	  
--EXEC xp_cmdshell @bcpCommand, no_output;
EXEC xp_cmdshell @bcpCommand;
RETURN 1;

END
GO
	

	--SELECT * FROM [PDFparser].[dbo].[exported_data]