USE [PDFparser]
    GO

    DROP TABLE IF EXISTS [dbo].[Agregate_Message];
    GO

    CREATE TABLE [dbo].[Agregate_Message](
        [id] [int] IDENTITY(1,1) NOT NULL,
		[Files_identified_total] [int] NULL,
		[Date_from] VARCHAR (50) NULL,
		[Date_into] VARCHAR (50) NULL,
        [Files_downloaded_total] [int] NULL,
		[Files_to_process_total] [int] NULL,
        [Files_parsed_total] [int] NULL,
        [Files_staged_total] [int] NULL,
        [Rows_inserted_total] [int] NULL,
        [Rows_with_error_total] [int] NULL,
		[Rows_need_enrichment_total] [int] NULL,
        [Started] [datetime] NULL,
        [Finished] [datetime] NULL,
        [Duration_in_seconds] [int] NULL
    CONSTRAINT [PK_Agregate_Message] PRIMARY KEY CLUSTERED 
    (
        [id] ASC
    )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
    ) ON [PRIMARY];
    GO

    SET ANSI_NULLS ON;
    GO
    SET QUOTED_IDENTIFIER ON;
    GO

	DECLARE @Files_downloaded_total INT;
    DECLARE @id_last INT;

    SET @Files_downloaded_total = 
        (SELECT 
            CAST(SUBSTRING(
                [MessageDescription], 
                CHARINDEX('Downloaded ', [MessageDescription]) + 11, 
                CHARINDEX(' files', [MessageDescription]) - CHARINDEX('Downloaded ', [MessageDescription]) - 11
            ) AS INT)
        FROM 
            [dbo].[Logs]
        WHERE 
            [MessageDescription] LIKE 'Downloaded % files'
            AND [ID] = (
                SELECT MAX([ID]) 
                FROM [dbo].[Logs]
                WHERE [MessageDescription] LIKE 'Downloaded % files'
            )
        );

    SET @id_last = 
        (SELECT MAX([ID]) 
        FROM [dbo].[Logs]
        WHERE [MessageDescription] LIKE 'Started time:%');

    --SELECT @id_last AS id_last;
    --SELECT @Files_downloaded_total AS Files_downloaded_total;

	DECLARE @Files_identified_total INT;

	SET @Files_identified_total = (
		SELECT TOP 1
			TRY_CAST(
				SUBSTRING(
					[MessageDescription],
					LEN('Identified ') + 1,
					CHARINDEX(' files to be loaded:', [MessageDescription]) - LEN('Identified ')
				) AS INT
			)
		FROM [dbo].[Logs]
		WHERE [MessageDescription] LIKE 'Identified % files to be loaded:%'
		  AND [ID] >= @id_last + 1
		ORDER BY [ID] DESC
	);

	--SELECT @Files_identified_total AS Files_identified_total;

	DECLARE @Files_to_process_total INT;

	WITH FileList AS (
		SELECT
			SUBSTRING([MessageDescription], CHARINDEX(':', [MessageDescription]) + 2, LEN([MessageDescription])) AS FileString
		FROM [Logs]
		WHERE [MessageDescription] LIKE 'Files to process: %'
        AND [ID] >= @id_last
	)
	SELECT @Files_to_process_total = COUNT(*)
	FROM FileList
	CROSS APPLY STRING_SPLIT(REPLACE(REPLACE(REPLACE(FileString, '[', ''), ']', ''), '''', ''), ',');

	--SELECT @Files_to_process_total AS Files_to_process_total;

    DECLARE @Files_parsed_total INT;

    SET @Files_parsed_total = 
        (SELECT COUNT(*)
        FROM [dbo].[Logs]
        WHERE [MessageDescription] LIKE 'Parsing file%'
        AND [ID] >= @id_last
        ) / 2;

    ---- Output the result for verification
    --SELECT @Files_parsed_total AS Files_parsed_total;


    DECLARE @Files_staged_total INT;

    SET @Files_staged_total = 
        (SELECT COUNT(*)
        FROM [dbo].[Logs]
        WHERE [MessageDescription] LIKE 'Staging file%'
        AND [ID] >= @id_last
        ) / 2;

    ---- Output the result for verification
    --SELECT @Files_staged_total AS Files_staged_total;

DECLARE @Rows_inserted_total INT;

SET @Rows_inserted_total = 
(
    SELECT SUM(TRY_CAST(
            LTRIM(RTRIM(SUBSTRING([MessageDescription], LEN('Inserted rows:') + 1, 100)))
        AS INT))
    FROM [dbo].[Logs]
    WHERE [MessageDescription] LIKE 'Inserted rows:%'
      AND [ID] >= @id_last
);

---- Output the result for verification
--SELECT @Rows_inserted_total AS Rows_inserted_total;

DECLARE @Rows_with_error_total INT;

SET @Rows_with_error_total = 
(
    SELECT SUM(TRY_CAST(
            LTRIM(RTRIM(SUBSTRING([MessageDescription], LEN('Rows with errors:') + 1, 100)))
        AS INT))
    FROM [dbo].[Logs]
    WHERE [MessageDescription] LIKE 'Rows with errors:%'
      AND [ID] >= @id_last
);

---- Output the result for verification
--SELECT @Rows_with_error_total AS Rows_with_error_total;


DECLARE @Rows_need_enrichment_total INT;

SET @Rows_need_enrichment_total = 
(
    SELECT SUM(TRY_CAST(
            LTRIM(RTRIM(SUBSTRING([MessageDescription], LEN('Rows need enrichment:') + 1, 100)))
        AS INT))
    FROM [dbo].[Logs]
    WHERE [MessageDescription] LIKE 'Rows need enrichment:%' 
      AND [ID] >= @id_last
);

---- Output the result for verification
--SELECT @Rows_need_enrichment_total AS Rows_need_enrichment_total;


DECLARE @Started datetime;

SET @Started = (
    SELECT MAX(TRY_CAST(
        LTRIM(RTRIM(SUBSTRING([MessageDescription], LEN('Started time:') + 1, 100)))
        AS datetime))
    FROM [dbo].[Logs]
    WHERE [MessageDescription] LIKE 'Started time:%'
      AND [ID] >= @id_last-2
);

--SELECT @Started AS Started;

DECLARE @Finished datetime;

SET @Finished = (
    SELECT MAX(TRY_CAST(
        LTRIM(RTRIM(SUBSTRING([MessageDescription], LEN('Finished time:') + 1, 100)))
        AS datetime))
    FROM [dbo].[Logs]
    WHERE [MessageDescription] LIKE 'Finished time:%'
      AND [ID] >= @id_last
);

--SELECT @Finished AS Finished;

DECLARE @Duration int;

SET @Duration = DATEDIFF(SECOND, @Started, @Finished);

--SELECT @Duration AS DurationSeconds;

DECLARE @Date_from VARCHAR(50);

	SET @Date_from = (
		SELECT TOP 1
			LTRIM(RTRIM(SUBSTRING([MessageDescription], LEN('Date_from:') + 1, 100)))
		FROM [dbo].[Logs]
		WHERE [MessageDescription] LIKE 'Date_from:%'
		  AND [ID] >= @id_last
	);

	--SELECT @Date_from AS Date_from;

	DECLARE @Date_into VARCHAR(50);

	SET @Date_into = (
		SELECT TOP 1
			LTRIM(RTRIM(SUBSTRING([MessageDescription], LEN('Date_into:') + 1, 100)))
		FROM [dbo].[Logs]
		WHERE [MessageDescription] LIKE 'Date_into:%'
		  AND [ID] >= @id_last
	);

	--SELECT @Date_into AS Date_into;



INSERT INTO [dbo].[Agregate_Message] (
	Files_identified_total,
	Date_from,
	Date_into,
    Files_downloaded_total,
	Files_to_process_total,
    Files_parsed_total,
    Files_staged_total,
    Rows_inserted_total,
    Rows_with_error_total,
	Rows_need_enrichment_total,
    Started,
    Finished,
    Duration_in_seconds
)
VALUES (
	@Files_identified_total,
	@Date_from,
	@Date_into,
    @Files_downloaded_total,
	@Files_to_process_total,
    @Files_parsed_total,
    @Files_staged_total,
    @Rows_inserted_total,
    @Rows_with_error_total,
	@Rows_need_enrichment_total,
    @Started,
    @Finished,
    @Duration
);






DECLARE @SlackMessage VARCHAR(4000);

SELECT TOP 1
    @SlackMessage = CONCAT(
        '#servername# \n--- Aggregate Message ---\n',
		'Files_identified_to_load_total: ', ISNULL(Files_identified_total, 0),
		' (Most recent dates: [', ISNULL(Date_from, 0), '] -> [',
		 ISNULL(Date_into, 0), ']) \n',
        'Files downloaded total : ', ISNULL(Files_downloaded_total, 0), ' \n',
		'Files to process total : ', ISNULL(Files_to_process_total, 0), ' \n',
        'Files parsed total     : ', ISNULL(Files_parsed_total, 0), ' \n',
        'Files staged total     : ', ISNULL(Files_staged_total, 0), ' \n',
        'Rows inserted total    : ', ISNULL(Rows_inserted_total, 0), ' \n',
        'Rows with error total (in all tables) : ', ISNULL(Rows_with_error_total, 0), ' \n',
		'Rows need enrichment total (in all tables) : ', ISNULL(Rows_need_enrichment_total, 0), ' \n',
        'Beginning time    : ', FORMAT(Started, 'yyyy-MM-dd HH:mm:ss'), ' \n',
        'Finished              : ', FORMAT(Finished, 'yyyy-MM-dd HH:mm:ss'), ' \n',
        'Duration (seconds)    : ', ISNULL(Duration_in_seconds, 0), ' \n'
    )
FROM [dbo].[Agregate_Message]
ORDER BY id DESC;

 EXEC [PDFparser].dbo.Monitor_SendSlackMessage 'Eva Iablocova', @SlackMessage;
