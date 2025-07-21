SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
/*===================================================================================================================
 Stored Procedure  : dbo.Dedupe_Staging_Records
 Author				: Boris Galcenco
 Create Date		: 21 JUL 2025

 Purpose			: Deduplicates and DELETE's duplicated records, leaving the most recent record
 Input Parameters	: @TableName

 Output Parameters  : None

 Usage				: EXEC PDFparser.dbo.Dedupe_Staging_Records 'ALL'
					  EXEC PDFparser.dbo.Dedupe_Staging_Records 'staging_Denumirea'

 Called By			: 

 Revision History
 Name				Date      Description
 ---------------------------------------------------------------------------------------------------------------------
 Boris Galcenco		21 JUL 2025    [POC]:PDF parser - Initial Development
 
=====================================================================================================================*/
CREATE OR ALTER PROCEDURE [dbo].[Dedupe_Staging_Records]
  @TableName VARCHAR(200) = NULL
  
AS
BEGIN
	SET NOCOUNT ON;


	-------------------------------------------------------------------------
	IF @TableName IN( 'ALL','staging_Denumirea')
	BEGIN
		;WITH DedupeRecords AS (
			SELECT *
				,RN = ROW_NUMBER() OVER (Partition By [No],[Date_of_announcement],[IDNO],[Name],[Address],[Name_From],[Name_Into] ORDER BY [Id] Desc)
			FROM staging_Denumirea
			)
		DELETE FROM DedupeRecords
		WHERE RN > 1

		PRINT 'Cleaned table:[staging_Denumirea]'
	END

	-------------------------------------------------------------------------
	IF @TableName IN( 'ALL','staging_Finaliz_proced_reorg')
	BEGIN
		;WITH DedupeRecords AS (
			SELECT *
				,RN = ROW_NUMBER() OVER (Partition By [No],[Date_of_announcement],[IDNO],[Name],[Type_of_reorganization],[Successors_of_rights] ORDER BY [Id] Desc)
			FROM staging_Finaliz_proced_reorg
			)
		DELETE FROM DedupeRecords
		WHERE RN > 1

		PRINT 'Cleaned table:[staging_Finaliz_proced_reorg]'
	END

	-------------------------------------------------------------------------
	IF @TableName IN( 'ALL','staging_Inactive')
	BEGIN
		;WITH DedupeRecords AS (
			SELECT *
				,RN = ROW_NUMBER() OVER (Partition By [No],[Date_of_announcement],[IDNO],[Name],[Address],[Date_of_dissolution] ORDER BY [Id] Desc)
			FROM staging_Inactive
			)
		DELETE FROM DedupeRecords
		WHERE RN > 1

		PRINT 'Cleaned table:[staging_Inactive]'
	END

	-------------------------------------------------------------------------
	IF @TableName IN( 'ALL','staging_Init_lichid')
	BEGIN
		;WITH DedupeRecords AS (
			SELECT *
				,RN = ROW_NUMBER() OVER (Partition By [No],[Date_of_announcement],[IDNO],[Name],[Address] ORDER BY [Id] Desc)
			FROM staging_Init_lichid
			)
		DELETE FROM DedupeRecords
		WHERE RN > 1

		PRINT 'Cleaned table:[staging_Init_lichid]'
	END

	-------------------------------------------------------------------------
	IF @TableName IN( 'ALL','staging_Init_reorg')
	BEGIN
		;WITH DedupeRecords AS (
			SELECT *
				,RN = ROW_NUMBER() OVER (Partition By [No],[Date_of_announcement],[IDNO],[Name],[Type_of_reorganization_1],[Type_of_reorganization_2],[Address] ORDER BY [Id] Desc)
			FROM staging_Init_reorg
			)
		DELETE FROM DedupeRecords
		WHERE RN > 1

		PRINT 'Cleaned table:[staging_Init_reorg]'
	END

	-------------------------------------------------------------------------
	IF @TableName IN( 'ALL','staging_Lichidarea')
	BEGIN
		;WITH DedupeRecords AS (
			SELECT *
				,RN = ROW_NUMBER() OVER (Partition By [No],[Date_of_announcement],[IDNO],[Name],[Address],[Date_of_deregistretion] ORDER BY [Id] Desc)
			FROM staging_Lichidarea
			)
		DELETE FROM DedupeRecords
		WHERE RN > 1

		PRINT 'Cleaned table:[staging_Lichidarea]'
	END

	-------------------------------------------------------------------------
	IF @TableName IN( 'ALL','staging_Reducere')
	BEGIN
		;WITH DedupeRecords AS (
			SELECT *
				,RN = ROW_NUMBER() OVER (Partition By [No],[Date_of_announcement],[IDNO],[Name],[Address],[Price_From],[Price_Into] ORDER BY [Id] Desc)
			FROM staging_Reducere
			)
		DELETE FROM DedupeRecords
		WHERE RN > 1

		PRINT 'Cleaned table:[staging_Reducere]'
	END

	-------------------------------------------------------------------------
	IF @TableName IN( 'ALL','staging_Sediul')
	BEGIN
		;WITH DedupeRecords AS (
			SELECT *
				,RN = ROW_NUMBER() OVER (Partition By [No],[Date_of_announcement],[IDNO],[Name],[Address],[Address_From],[Address_Into] ORDER BY [Id] Desc)
			FROM staging_Sediul
			)
		DELETE FROM DedupeRecords
		WHERE RN > 1

		PRINT 'Cleaned table:[staging_Sediul]'
	END


-- SP end --
END	 
GO
