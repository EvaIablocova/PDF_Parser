DECLARE 
	@attempt INT = 1, 
	@max_attempts INT = 3, 
	@delay_minutes NVARCHAR(8) = '00:05:00',
	@last_started_id BIGINT,
	@last_finished_id BIGINT


	WHILE @attempt <= @max_attempts
	BEGIN

		SELECT TOP 1 @last_started_id = [ID]
		FROM [PDFparser].[dbo].[Logs]
		WHERE [MessageDescription] LIKE 'Started time:%'
		ORDER BY [ID] DESC;

		SELECT TOP 1 @last_finished_id = [ID]
		FROM [PDFparser].[dbo].[Logs]
		WHERE [MessageDescription] LIKE 'Finished time:%'
		ORDER BY [ID] DESC;

		PRINT @last_started_id
		PRINT @last_finished_id

		IF @last_finished_id > @last_started_id
			BREAK;

		PRINT @attempt

		IF @attempt = @max_attempts 
			BEGIN
				INSERT INTO [PDFparser].[dbo].[Logs] ([DateInserted], [ExecutionStep], [MessageDescription])
				VALUES (GETDATE(), 'SQL Export', N'Error: Import is going now');
				THROW 51000, N'Error: Import is going now', 1;
			END

		WAITFOR DELAY @delay_minutes;
		SET @attempt += 1;
	END

	--PRINT 'Step 1 finished'