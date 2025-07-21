    USE [PDFparser]
    GO
    
    INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
    VALUES ('SQL Validator', 'Finaliz_proced_reorg [start]')
    GO

    INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
    SELECT 
        'SQL INFO status', 
        --'Inserted rows: ' + CAST(COUNT(1) AS NVARCHAR) + ' into [dbo].[Finaliz_proced_reorg]'
		'Inserted rows: ' + CAST(COUNT(1) AS NVARCHAR)
    FROM [dbo].[Finaliz_proced_reorg]
    WHERE is_valid IS NULL;
    GO

    UPDATE [dbo].[Finaliz_proced_reorg]
    SET 
        is_valid = 0,
        error_message = 
            ISNULL(error_message, '') +
            CASE WHEN ISNUMERIC([No]) = 0 THEN '[No] is not numeric;' ELSE '' END +
            CASE WHEN [Date_of_announcement] IS NULL THEN 'Date is NULL; ' ELSE '' END +
            CASE WHEN LTRIM(RTRIM([Date_of_announcement])) = '' THEN 'Date is empty; ' ELSE '' END +
            CASE WHEN TRY_CONVERT(DATE, [Date_of_announcement], 104) IS NULL THEN 'Invalid date; ' ELSE '' END +
            CASE WHEN [IDNO] NOT LIKE '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]' THEN 'IDNO is not 13-digit number; ' ELSE '' END +
            CASE WHEN LEFT([Name], CHARINDEX(' ', [Name] + ' ') - 1) NOT IN ('Societatea', 'Întreprinderea', 'CA', 'Centrul', 'Publicația', 'Firma', 'Casa') THEN '[Name] does not start with valid organization type; ' ELSE '' END +
            CASE WHEN LEFT([Type_of_reorganization], CHARINDEX(' ', [Type_of_reorganization] + ' ') - 1) NOT IN ('Transformare', 'Dezmembrare', 'Fuziune', 'Separare') THEN 'Invalid first word in [Type_of_reorganization]; ' ELSE '' END +
            CASE WHEN [Successors_of_rights] NOT LIKE '%(IDNO%[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9])%' THEN 'Missing (IDNO ...) at the end [Successors_of_rights]; ' ELSE '' END
    WHERE
        is_valid IS NULL
        AND ( 
            1=0
            OR ISNUMERIC([No]) = 0
            OR [Date_of_announcement] IS NULL
            OR LTRIM(RTRIM([Date_of_announcement])) = ''
            OR TRY_CONVERT(DATE, [Date_of_announcement], 104) IS NULL
            OR [IDNO] NOT LIKE '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'
            OR LEFT([Name], CHARINDEX(' ', [Name] + ' ') - 1) NOT IN ('Societatea', 'Întreprinderea', 'CA', 'Centrul', 'Publicația', 'Firma', 'Casa')
            OR LEFT([Type_of_reorganization], CHARINDEX(' ', [Type_of_reorganization] + ' ') - 1) NOT IN ('Transformare', 'Dezmembrare', 'Fuziune', 'Separare')
            OR [Successors_of_rights] NOT LIKE '%(IDNO%[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9])%'
        );
    
    UPDATE [dbo].[Finaliz_proced_reorg]
    SET 
        is_valid = 1
    WHERE
        is_valid IS NULL
        AND NOT (
            ISNUMERIC([No]) = 0
            OR [Date_of_announcement] IS NULL
            OR LTRIM(RTRIM([Date_of_announcement])) = ''
            OR TRY_CONVERT(DATE, [Date_of_announcement], 104) IS NULL
            OR [IDNO] NOT LIKE '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'
            OR LEFT([Name], CHARINDEX(' ', [Name] + ' ') - 1) NOT IN ('Societatea', 'Întreprinderea', 'CA', 'Centrul', 'Publicația', 'Firma', 'Casa')
            OR LEFT([Type_of_reorganization], CHARINDEX(' ', [Type_of_reorganization] + ' ') - 1) NOT IN ('Transformare', 'Dezmembrare', 'Fuziune', 'Separare')
            OR [Successors_of_rights] NOT LIKE '%(IDNO%[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9])%'
        );
    GO

    INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
    SELECT 
        'SQL INFO status', 
        --'Rows with errors: ' + CAST(COUNT(1) AS NVARCHAR) + ' in [dbo].[Finaliz_proced_reorg]'
		'Rows with errors: ' + CAST(COUNT(1) AS NVARCHAR)
    FROM [dbo].[Finaliz_proced_reorg]
    WHERE is_valid = 0;
    GO

	INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
    SELECT 
        'SQL INFO status', 
        'Rows need enrichment: ' + CAST(COUNT(1) AS NVARCHAR)
    FROM [dbo].[Finaliz_proced_reorg]
    WHERE is_valid = 1
		AND error_message != '';
    GO

    INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
    VALUES ('SQL Validator', 'Finaliz_proced_reorg [done]')
    GO

    INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
    VALUES ('SQL Validator', 'Denumirea [start]')
    GO


    INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
    SELECT 
        'SQL INFO status', 
        --'Inserted rows: ' + CAST(COUNT(1) AS NVARCHAR) + ' into [dbo].[Denumirea]'
		'Inserted rows: ' + CAST(COUNT(1) AS NVARCHAR)
    FROM [dbo].[Denumirea]
    WHERE is_valid IS NULL;
    GO

    UPDATE [dbo].[Denumirea]
    SET 
        is_valid = 0,
        error_message = 
            ISNULL(error_message, '') +
            CASE WHEN ISNUMERIC([No]) = 0 THEN '[No] is not numeric;' ELSE '' END +
            CASE WHEN [Date_of_announcement] IS NULL THEN 'Date is NULL; ' ELSE '' END +
            CASE WHEN LTRIM(RTRIM([Date_of_announcement])) = '' THEN 'Date is empty; ' ELSE '' END +
            CASE WHEN TRY_CONVERT(DATE, [Date_of_announcement], 104) IS NULL THEN 'Invalid date; ' ELSE '' END +
            CASE WHEN LEN([IDNO]) <> 13 OR [IDNO] LIKE '%[^0-9]%' THEN 'IDNO is not 13-digit number; ' ELSE '' END +
            -- CASE WHEN LEFT([Name], CHARINDEX(' ', [Name] + ' ') - 1) COLLATE Latin1_General_CI_AI
            --     NOT IN ('Societatea', 'Societate', 'Întreprinderea', 'CA', 'Centrul', 'Publicatia', 'Firma', 'Casa', 'Asociatia', 'INSTITUTIA', 'INSTITUŢIA', 'Broker', 'Brokerul', 'Şcoala', 'Organizaţia', 'Clubul', 'Agent', 'INSTITUTUL', 'RESTAURANTUL') 
            --     THEN '[Name] does not start with valid organization type; ' ELSE '' END +
            CASE WHEN LEFT([Address],  CHARINDEX(' ', [Address] + ' ') - 1) NOT LIKE '%MD-[0-9][0-9][0-9][0-9]%' THEN '[Address] does not start with ''MD-...''; ' ELSE '' END +
            CASE WHEN [Name] != [Name_Into] THEN '[Name] != [Name_Into]' ELSE '' END
    WHERE
        is_valid IS NULL
        AND ( 
            1=0
            OR ISNUMERIC([No]) = 0
            OR [Date_of_announcement] IS NULL
            OR LTRIM(RTRIM([Date_of_announcement])) = ''
            OR TRY_CONVERT(DATE, [Date_of_announcement], 104) IS NULL
            OR LEN([IDNO]) <> 13 OR [IDNO] LIKE '%[^0-9]%'
            -- OR (LEFT([Name], CHARINDEX(' ', [Name] + ' ') - 1) COLLATE Latin1_General_CI_AI
            --     NOT IN ('Societatea', 'Societate', 'Întreprinderea', 'CA', 'Centrul', 'Publicatia', 'Firma', 'Casa', 'Asociatia', 'INSTITUTIA', 'INSTITUŢIA', 'Broker', 'Brokerul', 'Şcoala', 'Organizaţia', 'Clubul', 'Agent', 'INSTITUTUL', 'RESTAURANTUL'))     
            OR LEFT([Address],  CHARINDEX(' ', [Address] + ' ') - 1) NOT LIKE '%MD-[0-9][0-9][0-9][0-9]%'
            OR [Name] != [Name_Into]
        );
    GO

    UPDATE [dbo].[Denumirea]
    SET 
        is_valid = 1
    WHERE
        is_valid IS NULL
        AND NOT (
            1=0
            OR ISNUMERIC([No]) = 0
            OR [Date_of_announcement] IS NULL
            OR LTRIM(RTRIM([Date_of_announcement])) = ''
            OR TRY_CONVERT(DATE, [Date_of_announcement], 104) IS NULL
            OR LEN([IDNO]) <> 13 OR [IDNO] LIKE '%[^0-9]%'
            -- OR (LEFT([Name], CHARINDEX(' ', [Name] + ' ') - 1) COLLATE Latin1_General_CI_AI
            --     NOT IN ('Societatea', 'Societate', 'Întreprinderea', 'CA', 'Centrul', 'Publicatia', 'Firma', 'Casa', 'Asociatia', 'INSTITUTIA', 'Broker', 'Brokerul', 'Şcoala', 'Organizaţia', 'Clubul', 'Agent', 'INSTITUTUL', 'RESTAURANTUL'))     
            OR LEFT([Address],  CHARINDEX(' ', [Address] + ' ') - 1) NOT LIKE '%MD-[0-9][0-9][0-9][0-9]%'
            OR [Name] != [Name_Into]
        );
    GO

    INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
    SELECT 
        'SQL INFO status', 
        --'Rows with errors: ' + CAST(COUNT(1) AS NVARCHAR) + ' in [dbo].[Denumirea]'
		'Rows with errors: ' + CAST(COUNT(1) AS NVARCHAR)
    FROM [dbo].[Denumirea]
    WHERE is_valid = 0;
    GO

	INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
    SELECT 
        'SQL INFO status', 
        'Rows need enrichment: ' + CAST(COUNT(1) AS NVARCHAR)
    FROM [dbo].[Denumirea]
    WHERE is_valid = 1
		AND error_message != '';
    GO


    INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
    VALUES ('SQL Validator', 'Denumirea [done]')
    GO


    INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
    VALUES ('SQL Validator', 'Inactive [start]')
    GO

    INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
    SELECT 
        'SQL INFO status', 
        --'Inserted rows: ' + CAST(COUNT(1) AS NVARCHAR) + ' into [dbo].[Inactive]'
		'Inserted rows: ' + CAST(COUNT(1) AS NVARCHAR)
    FROM [dbo].[Inactive]
    WHERE is_valid IS NULL;
    GO

    UPDATE [dbo].[Inactive]
    SET 
        is_valid = 0,
        error_message = 
            ISNULL(error_message, '') +
            CASE WHEN ISNUMERIC([No]) = 0 THEN '[No] is not numeric;' ELSE '' END +
            CASE WHEN [Date_of_announcement] IS NULL THEN 'Date is NULL; ' ELSE '' END +
            CASE WHEN LTRIM(RTRIM([Date_of_announcement])) = '' THEN 'Date is empty; ' ELSE '' END +
            CASE WHEN TRY_CONVERT(DATE, [Date_of_announcement], 104) IS NULL THEN 'Invalid date; ' ELSE '' END +
            CASE WHEN LEN([IDNO]) <> 13 OR [IDNO] LIKE '%[^0-9]%' THEN 'IDNO is not 13-digit number; ' ELSE '' END +
            -- CASE WHEN LEFT([Name], CHARINDEX(' ', [Name] + ' ') - 1) COLLATE Latin1_General_CI_AI
            --     NOT IN ('Societatea', 'Societate', 'Întreprinderea', 'CA', 'Centrul', 'Publicatia', 'Firma', 'Casa', 'Asociatia', 'INSTITUTIA', 'Broker', 'Brokerul', 'Şcoala', 'Organizaţia', 'Clubul', 'Agent', 'INSTITUTUL', 'RESTAURANTUL') THEN '[Name] does not start with valid organization type; ' ELSE '' END +
            CASE WHEN LEFT([Address],  CHARINDEX(' ', [Address] + ' ') - 1) NOT LIKE '%MD-[0-9][0-9][0-9][0-9]%' THEN '[Address] does not start with ''MD-...''; ' ELSE '' END +
            CASE WHEN [Date_of_dissolution] IS NULL THEN '[Date_of_dissolution] is NULL; ' ELSE '' END +
            CASE WHEN LTRIM(RTRIM([Date_of_dissolution])) = '' THEN '[Date_of_dissolution] is empty; ' ELSE '' END +
            CASE WHEN TRY_CONVERT(DATE, [Date_of_dissolution], 104) IS NULL THEN 'Invalid [Date_of_dissolution]; ' ELSE '' END +
            CASE WHEN [Date_of_dissolution] != [Date_of_announcement] THEN '[Date_of_dissolution] != [Date_of_announcement]' ELSE '' END
    WHERE
        is_valid IS NULL
        AND (  
            1=0
            OR ISNUMERIC([No]) = 0
            OR [Date_of_announcement] IS NULL
            OR LTRIM(RTRIM([Date_of_announcement])) = ''
            OR TRY_CONVERT(DATE, [Date_of_announcement], 104) IS NULL
            OR LEN([IDNO]) <> 13 OR [IDNO] LIKE '%[^0-9]%'
            -- OR (LEFT([Name], CHARINDEX(' ', [Name] + ' ') - 1) COLLATE Latin1_General_CI_AI
            --     NOT IN ('Societatea', 'Societate', 'Întreprinderea', 'CA', 'Centrul', 'Publicatia', 'Firma', 'Casa', 'Asociatia', 'INSTITUTIA', 'Broker', 'Brokerul', 'Şcoala', 'Organizaţia', 'Clubul', 'Agent', 'INSTITUTUL', 'RESTAURANTUL'))     
            OR LEFT([Address],  CHARINDEX(' ', [Address] + ' ') - 1) NOT LIKE '%MD-[0-9][0-9][0-9][0-9]%'
            OR [Date_of_dissolution] IS NULL
            OR LTRIM(RTRIM([Date_of_dissolution])) = ''
            OR TRY_CONVERT(DATE, [Date_of_dissolution], 104) IS NULL
            OR [Date_of_dissolution] != [Date_of_announcement]
        );
    GO

    UPDATE [dbo].[Inactive]
    SET 
        is_valid = 1
    WHERE
        is_valid IS NULL
        AND NOT (
            1=0
            OR ISNUMERIC([No]) = 0
            OR [Date_of_announcement] IS NULL
            OR LTRIM(RTRIM([Date_of_announcement])) = ''
            OR TRY_CONVERT(DATE, [Date_of_announcement], 104) IS NULL
            OR LEN([IDNO]) <> 13 OR [IDNO] LIKE '%[^0-9]%'
            -- OR (LEFT([Name], CHARINDEX(' ', [Name] + ' ') - 1) COLLATE Latin1_General_CI_AI
            --     NOT IN ('Societatea', 'Societate', 'Întreprinderea', 'CA', 'Centrul', 'Publicatia', 'Firma', 'Casa', 'Asociatia', 'INSTITUTIA', 'Broker', 'Brokerul', 'Şcoala', 'Organizaţia', 'Clubul', 'Agent', 'INSTITUTUL', 'RESTAURANTUL'))     
            OR LEFT([Address],  CHARINDEX(' ', [Address] + ' ') - 1) NOT LIKE '%MD-[0-9][0-9][0-9][0-9]%'
            OR [Date_of_dissolution] IS NULL
            OR LTRIM(RTRIM([Date_of_dissolution])) = ''
            OR TRY_CONVERT(DATE, [Date_of_dissolution], 104) IS NULL
            OR [Date_of_dissolution] != [Date_of_announcement]
        );
    GO

    INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
    SELECT 
        'SQL INFO status', 
        --'Rows with errors: ' + CAST(COUNT(1) AS NVARCHAR) + ' in [dbo].[Inactive]'
		'Rows with errors: ' + CAST(COUNT(1) AS NVARCHAR)
    FROM [dbo].[Inactive]
    WHERE is_valid = 0;
    GO

	INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
    SELECT 
        'SQL INFO status', 
        'Rows need enrichment: ' + CAST(COUNT(1) AS NVARCHAR)
    FROM [dbo].[Inactive]
    WHERE is_valid = 1
		AND error_message != '';
    GO

    INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
    VALUES ('SQL Validator', 'Inactive [done]')
    GO

    INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
    VALUES ('SQL Validator', 'Init_lichid [start]')
    GO

    INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
    SELECT 
        'SQL INFO status', 
        --'Inserted rows: ' + CAST(COUNT(1) AS NVARCHAR) + ' into [dbo].[Init_lichid]'
		'Inserted rows: ' + CAST(COUNT(1) AS NVARCHAR)
    FROM [dbo].[Init_lichid]
    WHERE is_valid IS NULL;
    GO

    UPDATE [dbo].[Init_lichid]
    SET 
        is_valid = 0,
        error_message = 
            ISNULL(error_message, '') +
            CASE WHEN ISNUMERIC([No]) = 0 THEN '[No] is not numeric;' ELSE '' END +
            CASE WHEN [Date_of_announcement] IS NULL THEN 'Date is NULL; ' ELSE '' END +
            CASE WHEN LTRIM(RTRIM([Date_of_announcement])) = '' THEN 'Date is empty; ' ELSE '' END +
            CASE WHEN TRY_CONVERT(DATE, [Date_of_announcement], 104) IS NULL THEN 'Invalid date; ' ELSE '' END +
            CASE WHEN LEN([IDNO]) <> 13 OR [IDNO] LIKE '%[^0-9]%' THEN 'IDNO is not 13-digit number; ' ELSE '' END +
            -- CASE WHEN LEFT([Name], CHARINDEX(' ', [Name] + ' ') - 1) COLLATE Latin1_General_CI_AI
            --     NOT IN ('Societatea', 'Societate', 'Întreprinderea', 'CA', 'Centrul', 'Publicatia', 'Firma', 'Casa', 'Asociatia', 'INSTITUTIA', 'Broker', 'Brokerul', 'Şcoala', 'Organizaţia', 'Clubul', 'Agent', 'INSTITUTUL', 'RESTAURANTUL') THEN '[Name] does not start with valid organization type; ' ELSE '' END +
            CASE WHEN LEFT([Address],  CHARINDEX(' ', [Address] + ' ') - 1) NOT LIKE '%MD-[0-9][0-9][0-9][0-9]%' THEN '[Address] does not start with ''MD-...''; ' ELSE '' END
    WHERE
        is_valid IS NULL
        AND (  
            1=0
            OR ISNUMERIC([No]) = 0
            OR [Date_of_announcement] IS NULL
            OR LTRIM(RTRIM([Date_of_announcement])) = ''
            OR TRY_CONVERT(DATE, [Date_of_announcement], 104) IS NULL
            OR LEN([IDNO]) <> 13 OR [IDNO] LIKE '%[^0-9]%'
            -- OR (LEFT([Name], CHARINDEX(' ', [Name] + ' ') - 1) COLLATE Latin1_General_CI_AI
            --     NOT IN ('Societatea', 'Societate', 'Întreprinderea', 'CA', 'Centrul', 'Publicatia', 'Firma', 'Casa', 'Asociatia', 'INSTITUTIA', 'Broker', 'Brokerul', 'Şcoala', 'Organizaţia', 'Clubul', 'Agent', 'INSTITUTUL', 'RESTAURANTUL'))     
            OR LEFT([Address],  CHARINDEX(' ', [Address] + ' ') - 1) NOT LIKE '%MD-[0-9][0-9][0-9][0-9]%'
        );
    GO

    UPDATE [dbo].[Init_lichid]
    SET 
        is_valid = 1
    WHERE
        is_valid IS NULL
        AND NOT (
            1=0
            OR ISNUMERIC([No]) = 0
            OR [Date_of_announcement] IS NULL
            OR LTRIM(RTRIM([Date_of_announcement])) = ''
            OR TRY_CONVERT(DATE, [Date_of_announcement], 104) IS NULL
            OR LEN([IDNO]) <> 13 OR [IDNO] LIKE '%[^0-9]%'
            -- OR (LEFT([Name], CHARINDEX(' ', [Name] + ' ') - 1) COLLATE Latin1_General_CI_AI
            --     NOT IN ('Societatea', 'Societate', 'Întreprinderea', 'CA', 'Centrul', 'Publicatia', 'Firma', 'Casa', 'Asociatia', 'INSTITUTIA', 'Broker', 'Brokerul', 'Şcoala', 'Organizaţia', 'Clubul', 'Agent', 'INSTITUTUL', 'RESTAURANTUL'))     
            OR LEFT([Address],  CHARINDEX(' ', [Address] + ' ') - 1) NOT LIKE '%MD-[0-9][0-9][0-9][0-9]%'
        );
    GO

    INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
    SELECT 
        'SQL INFO status', 
        --'Rows with errors: ' + CAST(COUNT(1) AS NVARCHAR) + ' in [dbo].[Init_lichid]'
		'Rows with errors: ' + CAST(COUNT(1) AS NVARCHAR)
    FROM [dbo].[Init_lichid]
    WHERE is_valid = 0;
    GO

	INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
    SELECT 
        'SQL INFO status', 
        'Rows need enrichment: ' + CAST(COUNT(1) AS NVARCHAR)
    FROM [dbo].[Init_lichid]
    WHERE is_valid = 1
		AND error_message != '';
    GO

    INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
    VALUES ('SQL Validator', 'Init_lichid [done]')
    GO


    INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
    VALUES ('SQL Validator', 'Init_reorg [start]')
    GO

    INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
    SELECT 
        'SQL INFO status', 
        --'Inserted rows: ' + CAST(COUNT(1) AS NVARCHAR) + ' into [dbo].[Init_reorg]'
		'Inserted rows: ' + CAST(COUNT(1) AS NVARCHAR)
    FROM [dbo].[Init_reorg]
    WHERE is_valid IS NULL;
    GO

    UPDATE [dbo].[Init_reorg]
    SET 
        is_valid = 0,
        error_message = 
            ISNULL(error_message, '') +
            CASE WHEN ISNUMERIC([No]) = 0 THEN '[No] is not numeric;' ELSE '' END +
            CASE WHEN [Date_of_announcement] IS NULL THEN 'Date is NULL; ' ELSE '' END +
            CASE WHEN LTRIM(RTRIM([Date_of_announcement])) = '' THEN 'Date is empty; ' ELSE '' END +
            CASE WHEN TRY_CONVERT(DATE, [Date_of_announcement], 104) IS NULL THEN 'Invalid date; ' ELSE '' END +
            CASE WHEN LEN([IDNO]) <> 13 OR [IDNO] LIKE '%[^0-9]%' THEN 'IDNO is not 13-digit number; ' ELSE '' END +
            CASE WHEN (LEFT([Type_of_reorganization_1], CHARINDEX(' ', [Type_of_reorganization_1] + ' ') - 1) NOT LIKE 'se') THEN '[Type_of_reorganization_1] does not start with ''se''; ' ELSE '' END +
            CASE WHEN LEFT([Name], CHARINDEX(' ', [Name] + ' ') - 1) COLLATE Latin1_General_CI_AI
                NOT IN ('ACADEMIA', 'ASOCIAŢIA', 'FIRMA', 'Instituţia', 'Întreprinderea', 'SOCIETATEA') THEN '[Name] does not start with valid organization type; ' ELSE '' END +
            CASE WHEN LEFT([Address],  CHARINDEX(' ', [Address] + ' ') - 1) NOT LIKE '%MD-[0-9][0-9][0-9][0-9]%' THEN '[Address] does not start with ''MD-...''; ' ELSE '' END
    WHERE
        is_valid IS NULL
        AND (  
            1=0
            OR ISNUMERIC([No]) = 0
            OR [Date_of_announcement] IS NULL
            OR LTRIM(RTRIM([Date_of_announcement])) = ''
            OR TRY_CONVERT(DATE, [Date_of_announcement], 104) IS NULL
            OR LEN([IDNO]) <> 13 OR [IDNO] LIKE '%[^0-9]%'
            OR (LEFT([Name], CHARINDEX(' ', [Name] + ' ') - 1)) 
                NOT IN ('ACADEMIA', 'ASOCIAŢIA', 'FIRMA', 'Instituţia', 'Întreprinderea', 'SOCIETATEA') 
            OR (LEFT([Type_of_reorganization_1], CHARINDEX(' ', [Type_of_reorganization_1] + ' ') - 1) NOT LIKE 'se')
            OR LEFT([Address],  CHARINDEX(' ', [Address] + ' ') - 1) NOT LIKE '%MD-[0-9][0-9][0-9][0-9]%'
        );
    GO

    UPDATE [dbo].[Init_reorg]
    SET 
        is_valid = 1
    WHERE
        is_valid IS NULL
        AND NOT (
            1=0
            OR ISNUMERIC([No]) = 0
            OR [Date_of_announcement] IS NULL
            OR LTRIM(RTRIM([Date_of_announcement])) = ''
            OR TRY_CONVERT(DATE, [Date_of_announcement], 104) IS NULL
            OR LEN([IDNO]) <> 13 OR [IDNO] LIKE '%[^0-9]%'
            OR (LEFT([Name], CHARINDEX(' ', [Name] + ' ') - 1)) 
                NOT IN ('ACADEMIA', 'ASOCIAŢIA', 'FIRMA', 'Instituţia', 'Întreprinderea', 'SOCIETATEA') 
            OR (LEFT([Type_of_reorganization_1], CHARINDEX(' ', [Type_of_reorganization_1] + ' ') - 1) NOT LIKE 'se')
            OR LEFT([Address],  CHARINDEX(' ', [Address] + ' ') - 1) NOT LIKE '%MD-[0-9][0-9][0-9][0-9]%'
        );
    GO

    INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
    SELECT 
        'SQL INFO status', 
        --'Rows with errors: ' + CAST(COUNT(1) AS NVARCHAR) + ' in [dbo].[Init_reorg]'
		'Rows with errors: ' + CAST(COUNT(1) AS NVARCHAR)
    FROM [dbo].[Init_reorg]
    WHERE is_valid = 0;
    GO

	INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
    SELECT 
        'SQL INFO status', 
        'Rows need enrichment: ' + CAST(COUNT(1) AS NVARCHAR)
    FROM [dbo].[Init_reorg]
    WHERE is_valid = 1
		AND error_message != '';
    GO

    INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
    VALUES ('SQL Validator', 'Init_reorg [done]')
    GO
    

    INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
    VALUES ('SQL Validator', 'Lichidarea [start]')
    GO

    INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
    SELECT 
        'SQL INFO status', 
        --'Inserted rows: ' + CAST(COUNT(1) AS NVARCHAR) + ' into [dbo].[Lichidarea]'
		'Inserted rows: ' + CAST(COUNT(1) AS NVARCHAR)

    FROM [dbo].[Lichidarea]
    WHERE is_valid IS NULL;
    GO

    UPDATE [dbo].[Lichidarea]
    SET 
        is_valid = 0,
        error_message = 
            ISNULL(error_message, '') +
            CASE WHEN ISNUMERIC([No]) = 0 THEN '[No] is not numeric;' ELSE '' END +
            CASE WHEN [Date_of_announcement] IS NULL THEN 'Date is NULL; ' ELSE '' END +
            CASE WHEN LTRIM(RTRIM([Date_of_announcement])) = '' THEN 'Date is empty; ' ELSE '' END +
            CASE WHEN TRY_CONVERT(DATE, [Date_of_announcement], 104) IS NULL THEN 'Invalid date; ' ELSE '' END +
            CASE WHEN LEN([IDNO]) <> 13 OR [IDNO] LIKE '%[^0-9]%' THEN 'IDNO is not 13-digit number; ' ELSE '' END +
            -- CASE WHEN LEFT([Name], CHARINDEX(' ', [Name] + ' ') - 1) COLLATE Latin1_General_CI_AI
            --     NOT IN ('Asociaţia', 'Casa', 'FIRMA', 'Societatea') THEN '[Name] does not start with valid organization type; ' ELSE '' END +
            CASE WHEN LEFT([Address],  CHARINDEX(' ', [Address] + ' ') - 1) NOT LIKE '%MD-[0-9][0-9][0-9][0-9]%' THEN '[Address] does not start with ''MD-...''; ' ELSE '' END +
            CASE WHEN [Date_of_deregistretion] IS NULL THEN '[Date_of_deregistretion] is NULL; ' ELSE '' END +
            CASE WHEN LTRIM(RTRIM([Date_of_deregistretion])) = '' THEN '[Date_of_deregistretion] is empty; ' ELSE '' END +
            CASE WHEN TRY_CONVERT(DATE, [Date_of_deregistretion], 104) IS NULL THEN 'Invalid [Date_of_deregistretion]; ' ELSE '' END +
            CASE WHEN [Date_of_deregistretion] != [Date_of_announcement] THEN '[Date_of_deregistretion] != [Date_of_announcement]' ELSE '' END
    WHERE
        is_valid IS NULL
        AND (  
            1=0
            OR ISNUMERIC([No]) = 0
            OR [Date_of_announcement] IS NULL
            OR LTRIM(RTRIM([Date_of_announcement])) = ''
            OR TRY_CONVERT(DATE, [Date_of_announcement], 104) IS NULL
            OR LEN([IDNO]) <> 13 OR [IDNO] LIKE '%[^0-9]%'
            -- OR (LEFT([Name], CHARINDEX(' ', [Name] + ' ') - 1))
            --     NOT IN ('Asociaţia', 'Casa', 'FIRMA', 'Societatea')    
            OR LEFT([Address],  CHARINDEX(' ', [Address] + ' ') - 1) NOT LIKE '%MD-[0-9][0-9][0-9][0-9]%'
            OR [Date_of_deregistretion] IS NULL
            OR LTRIM(RTRIM([Date_of_deregistretion])) = ''
            OR TRY_CONVERT(DATE, [Date_of_deregistretion], 104) IS NULL
            OR [Date_of_deregistretion] != [Date_of_announcement]
        );
    GO

    UPDATE [dbo].[Lichidarea]
    SET 
        is_valid = 1
    WHERE
        is_valid IS NULL
        AND NOT (
            1=0
            OR ISNUMERIC([No]) = 0
            OR [Date_of_announcement] IS NULL
            OR LTRIM(RTRIM([Date_of_announcement])) = ''
            OR TRY_CONVERT(DATE, [Date_of_announcement], 104) IS NULL
            OR LEN([IDNO]) <> 13 OR [IDNO] LIKE '%[^0-9]%'
            -- OR (LEFT([Name], CHARINDEX(' ', [Name] + ' ') - 1))
            --     NOT IN ('Asociaţia', 'Casa', 'FIRMA', 'Societatea')    
            OR LEFT([Address],  CHARINDEX(' ', [Address] + ' ') - 1) NOT LIKE '%MD-[0-9][0-9][0-9][0-9]%'
            OR [Date_of_deregistretion] IS NULL
            OR LTRIM(RTRIM([Date_of_deregistretion])) = ''
            OR TRY_CONVERT(DATE, [Date_of_deregistretion], 104) IS NULL
            OR [Date_of_deregistretion] != [Date_of_announcement]
        );
    GO

    INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
    SELECT 
        'SQL INFO status', 
        --'Rows with errors: ' + CAST(COUNT(1) AS NVARCHAR) + ' in [dbo].[Lichidarea]'
		'Rows with errors: ' + CAST(COUNT(1) AS NVARCHAR)
    FROM [dbo].[Lichidarea]
    WHERE is_valid = 0;
    GO

	INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
    SELECT 
        'SQL INFO status', 
        'Rows need enrichment: ' + CAST(COUNT(1) AS NVARCHAR)
    FROM [dbo].[Lichidarea]
    WHERE is_valid = 1
		AND error_message != '';
    GO

    INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
    VALUES ('SQL Validator', 'Lichidarea [done]')
    GO
    

    INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
    VALUES ('SQL Validator', 'Sediul [start]')
    GO

    INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
    SELECT 
        'SQL INFO status', 
        'Inserted rows: ' + CAST(COUNT(1) AS NVARCHAR)
    FROM [dbo].[Sediul]
    WHERE is_valid IS NULL;
    GO

    UPDATE [dbo].[Sediul]
    SET 
        is_valid = 0,
        error_message = 
            ISNULL(error_message, '') +
            CASE WHEN ISNUMERIC([No]) = 0 THEN '[No] is not numeric;' ELSE '' END +
            CASE WHEN [Date_of_announcement] IS NULL THEN 'Date is NULL; ' ELSE '' END +
            CASE WHEN LTRIM(RTRIM([Date_of_announcement])) = '' THEN 'Date is empty; ' ELSE '' END +
            CASE WHEN TRY_CONVERT(DATE, [Date_of_announcement], 104) IS NULL THEN 'Invalid date; ' ELSE '' END +
            CASE WHEN LEN([IDNO]) <> 13 OR [IDNO] LIKE '%[^0-9]%' THEN 'IDNO is not 13-digit number; ' ELSE '' END 
            -- CASE WHEN LEFT([Name], CHARINDEX(' ', [Name] + ' ') - 1) COLLATE Latin1_General_CI_AI
            --     NOT IN ('Societatea', 'Societate', 'Întreprinderea', 'CA', 'Centrul', 'Publicatia', 'Firma', 'Casa', 'Asociatia', 'INSTITUTIA', 'Broker', 'Brokerul', 'Şcoala', 'Organizaţia', 'Clubul', 'Agent', 'INSTITUTUL', 'RESTAURANTUL') THEN '[Name] does not start with valid organization type; ' ELSE '' END +
            -- CASE WHEN LEFT([Address],  CHARINDEX(' ', [Address] + ' ') - 1) NOT LIKE '%MD-[0-9][0-9][0-9][0-9]%' THEN '[Address] does not start with ''MD-...''; ' ELSE '' END +
            -- CASE WHEN LEFT([Address_From],  CHARINDEX(' ', [Address_From] + ' ') - 1) NOT LIKE '%MD-[0-9][0-9][0-9][0-9]%' THEN '[Address_From] does not start with ''MD-...''; ' ELSE '' END +
            -- CASE WHEN LEFT([Address_Into],  CHARINDEX(' ', [Address_Into] + ' ') - 1) NOT LIKE '%MD-[0-9][0-9][0-9][0-9]%' THEN '[Address_Into] does not start with ''MD-...''; ' ELSE '' END +
            -- CASE WHEN [Address] != [Address_Into] THEN '[Address] != [Address_Into]' ELSE '' END
    WHERE
        is_valid IS NULL
        AND (  
            1=0
            OR ISNUMERIC([No]) = 0
            OR [Date_of_announcement] IS NULL
            OR LTRIM(RTRIM([Date_of_announcement])) = ''
            OR TRY_CONVERT(DATE, [Date_of_announcement], 104) IS NULL
            OR LEN([IDNO]) <> 13 OR [IDNO] LIKE '%[^0-9]%'
            -- OR (LEFT([Name], CHARINDEX(' ', [Name] + ' ') - 1) COLLATE Latin1_General_CI_AI
            --     NOT IN ('Societatea', 'Societate', 'Întreprinderea', 'CA', 'Centrul', 'Publicatia', 'Firma', 'Casa', 'Asociatia', 'INSTITUTIA', 'Broker', 'Brokerul', 'Şcoala', 'Organizaţia', 'Clubul', 'Agent', 'INSTITUTUL', 'RESTAURANTUL'))     
            -- OR LEFT([Address],  CHARINDEX(' ', [Address] + ' ') - 1) NOT LIKE '%MD-[0-9][0-9][0-9][0-9]%'
            -- OR LEFT([Address_From],  CHARINDEX(' ', [Address] + ' ') - 1) NOT LIKE '%MD-[0-9][0-9][0-9][0-9]%'
            -- OR LEFT([Address_Into],  CHARINDEX(' ', [Address] + ' ') - 1) NOT LIKE '%MD-[0-9][0-9][0-9][0-9]%'
            -- OR [Address] != [Address_Into]
        );
    GO

	UPDATE [dbo].[Sediul]
    SET 
        is_valid = 1,
        error_message = 
            ISNULL(error_message, '') +
            CASE WHEN LEFT([Address],  CHARINDEX(' ', [Address] + ' ') - 1) NOT LIKE '%MD-[0-9][0-9][0-9][0-9]%' THEN '[Address] does not start with ''MD-...''; ' ELSE '' END +
            CASE WHEN LEFT([Address_From],  CHARINDEX(' ', [Address_From] + ' ') - 1) NOT LIKE '%MD-[0-9][0-9][0-9][0-9]%' THEN '[Address_From] does not start with ''MD-...''; ' ELSE '' END +
            CASE WHEN LEFT([Address_Into],  CHARINDEX(' ', [Address_Into] + ' ') - 1) NOT LIKE '%MD-[0-9][0-9][0-9][0-9]%' THEN '[Address_Into] does not start with ''MD-...''; ' ELSE '' END +
            CASE WHEN [Address] != [Address_Into] THEN '[Address] != [Address_Into]' ELSE '' END
    WHERE
        is_valid IS NULL
        AND (
            1=0  
            OR LEFT([Address],  CHARINDEX(' ', [Address] + ' ') - 1) NOT LIKE '%MD-[0-9][0-9][0-9][0-9]%'
            OR LEFT([Address_From],  CHARINDEX(' ', [Address] + ' ') - 1) NOT LIKE '%MD-[0-9][0-9][0-9][0-9]%'
            OR LEFT([Address_Into],  CHARINDEX(' ', [Address] + ' ') - 1) NOT LIKE '%MD-[0-9][0-9][0-9][0-9]%'
            OR [Address] != [Address_Into]
        );
    GO

    UPDATE [dbo].[Sediul]
    SET 
        is_valid = 1
    WHERE
        is_valid IS NULL
        AND NOT (
                        1=0
            OR ISNUMERIC([No]) = 0
            OR [Date_of_announcement] IS NULL
            OR LTRIM(RTRIM([Date_of_announcement])) = ''
            OR TRY_CONVERT(DATE, [Date_of_announcement], 104) IS NULL
            OR LEN([IDNO]) <> 13 OR [IDNO] LIKE '%[^0-9]%'
            -- OR (LEFT([Name], CHARINDEX(' ', [Name] + ' ') - 1) COLLATE Latin1_General_CI_AI
            --     NOT IN ('Societatea', 'Societate', 'Întreprinderea', 'CA', 'Centrul', 'Publicatia', 'Firma', 'Casa', 'Asociatia', 'INSTITUTIA', 'Broker', 'Brokerul', 'Şcoala', 'Organizaţia', 'Clubul', 'Agent', 'INSTITUTUL', 'RESTAURANTUL'))     
            OR LEFT([Address],  CHARINDEX(' ', [Address] + ' ') - 1) NOT LIKE '%MD-[0-9][0-9][0-9][0-9]%'
            OR LEFT([Address_From],  CHARINDEX(' ', [Address] + ' ') - 1) NOT LIKE '%MD-[0-9][0-9][0-9][0-9]%'
            OR LEFT([Address_Into],  CHARINDEX(' ', [Address] + ' ') - 1) NOT LIKE '%MD-[0-9][0-9][0-9][0-9]%'
            -- OR [Address] != [Address_Into]
        );
    GO




    INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
    SELECT 
        'SQL INFO status', 
        'Rows with errors: ' + CAST(COUNT(1) AS NVARCHAR)
    FROM [dbo].[Sediul]
    WHERE is_valid = 0;
    GO

	INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
    SELECT 
        'SQL INFO status', 
        'Rows need enrichment: ' + CAST(COUNT(1) AS NVARCHAR)
    FROM [dbo].[Sediul]
    WHERE is_valid = 1
		AND error_message != '';
    GO

    INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
    VALUES ('SQL Validator', 'Sediul [done]')
    GO


    INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
    VALUES ('SQL Validator', 'Reducere [start]')
    GO

    INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
    SELECT 
        'SQL INFO status', 
        --'Inserted rows: ' + CAST(COUNT(1) AS NVARCHAR) + ' into [dbo].[Reducere]'
		'Inserted rows: ' + CAST(COUNT(1) AS NVARCHAR)
    FROM [dbo].[Reducere]
    WHERE is_valid IS NULL;
    GO
  
    UPDATE [dbo].[Reducere]
    SET 
        is_valid = 0,
        error_message = 
            ISNULL(error_message, '') +
            CASE WHEN ISNUMERIC([No]) = 0 THEN '[No] is not numeric;' ELSE '' END +
            CASE WHEN [Date_of_announcement] IS NULL THEN 'Date is NULL; ' ELSE '' END +
            CASE WHEN LTRIM(RTRIM([Date_of_announcement])) = '' THEN 'Date is empty; ' ELSE '' END +
            CASE WHEN TRY_CONVERT(DATE, [Date_of_announcement], 104) IS NULL THEN 'Invalid date; ' ELSE '' END +
            CASE WHEN LEFT([Name], CHARINDEX(' ', [Name] + ' ') - 1) COLLATE Latin1_General_CI_AI
                NOT IN ('Casa', 'FIRMA', 'Societatea', 'Complexul', 'Întreprinderea') THEN '[Name] does not start with valid organization type; ' ELSE '' END +
            CASE WHEN LEN([IDNO]) <> 13 OR [IDNO] LIKE '%[^0-9]%' THEN 'IDNO is not 13-digit number; ' ELSE '' END
    WHERE
        is_valid IS NULL
        AND (  
            1=0
            OR ISNUMERIC([No]) = 0
            OR [Date_of_announcement] IS NULL
            OR LTRIM(RTRIM([Date_of_announcement])) = ''
            OR TRY_CONVERT(DATE, [Date_of_announcement], 104) IS NULL
            OR LEN([IDNO]) <> 13 OR [IDNO] LIKE '%[^0-9]%'
            OR (LEFT([Name], CHARINDEX(' ', [Name] + ' ') - 1))
                NOT IN ('Casa', 'FIRMA', 'Societatea', 'Complexul', 'Întreprinderea')
        );
    GO

    UPDATE [dbo].[Reducere]
    SET 
        is_valid = 1
    WHERE
        is_valid IS NULL
        AND NOT (
            1=0
            OR ISNUMERIC([No]) = 0
            OR [Date_of_announcement] IS NULL
            OR LTRIM(RTRIM([Date_of_announcement])) = ''
            OR TRY_CONVERT(DATE, [Date_of_announcement], 104) IS NULL
            OR LEN([IDNO]) <> 13 OR [IDNO] LIKE '%[^0-9]%'
            OR (LEFT([Name], CHARINDEX(' ', [Name] + ' ') - 1))
                NOT IN ('Casa', 'FIRMA', 'Societatea', 'Complexul', 'Întreprinderea')
        );
    GO

    INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
    SELECT 
        'SQL INFO status', 
        --'Rows with errors: ' + CAST(COUNT(1) AS NVARCHAR) + ' in [dbo].[Reducere]'
		'Rows with errors: ' + CAST(COUNT(1) AS NVARCHAR)
    FROM [dbo].[Reducere]
    WHERE is_valid = 0;
    GO

	INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
    SELECT 
        'SQL INFO status', 
        'Rows need enrichment: ' + CAST(COUNT(1) AS NVARCHAR)
    FROM [dbo].[Reducere]
    WHERE is_valid = 1
		AND error_message != '';
    GO

    INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
    VALUES ('SQL Validator', 'Reducere [done]')
    GO

	INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
	VALUES ('SQL Validator', 'Finished time: ' + CONVERT(varchar(19), GETDATE(), 120))
	GO


