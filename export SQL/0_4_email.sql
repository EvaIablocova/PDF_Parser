USE [PDFparser]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
/*===================================================================================================================
 Stored Procedure  : dbo.Send_Email_Exort

 Purpose      : Send Delta Files to Email Channels
 Input Parameters  : @Recipient, @File_name

 Output Parameters  : None

 Usage        : EXEC [PDFparser].dbo.Send_Email_Export 'a1l9e8x8eva@gmail.com','Denumirea'

=====================================================================================================================*/
CREATE OR ALTER PROCEDURE [dbo].[Send_Email_Export]
  @Recipient VARCHAR(100) = NULL,
  @File_name VARCHAR(100) = NULL
AS
BEGIN

  --DECLARE @File_name NVARCHAR(260)
  --SET @File_name = 'Denumirea'
  
  DECLARE 
    @TextSubject VARCHAR(200),
    @TextBody VARCHAR(500),
    @Year CHAR(4),
    @Week CHAR(2),
    @Today DATE = CAST(GETDATE() AS DATE),
	@LogMessage VARCHAR(200),
	@isExportedData BIT,
	@PathToExportedFile VARCHAR(500),
	@ExportFile NVARCHAR(260)


  -- Get current year and week
  SET @Year = FORMAT(GETDATE(), 'yyyy')
  SET @Week = FORMAT(DATEPART(ISO_WEEK, GETDATE()), '00')
  
  -- Build subject
  SET @TextSubject = 'PDFparser_exports_' + @File_name + '_' + @Year + '_' + @Week + ' week'

--PRINT @TextSubject


	EXEC @isExportedData = [PDFparser].dbo.Export_Delta_To_CSV @File_name

	SET @ExportFile = N'C:\Export\' + @File_name + '_' + CONVERT(NVARCHAR(8), @Today, 112) + '.csv';

	IF @isExportedData = 1
	BEGIN
		SET @PathToExportedFile = @ExportFile;
		SET @LogMessage = 'Delta exported to CSV in ' + @File_name;
	END
	ELSE
	BEGIN
		SET @TextBody = N'There is no data for export SQL';
		SET @LogMessage = 'No data to export SQL in ' + @File_name;
	END


	INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
	VALUES ('SQL Export', @LogMessage)

	IF @PathToExportedFile IS NULL
		EXEC msdb.dbo.sp_send_dbmail
			@profile_name = 'Eva Iablocova',
			@recipients = @Recipient,
			@subject = @TextSubject,
			@body = @TextBody;
	ELSE
		EXEC msdb.dbo.sp_send_dbmail
			@profile_name = 'Eva Iablocova',
			@recipients = @Recipient,
			@subject = @TextSubject,
			@file_attachments = @PathToExportedFile;

	UPDATE ETL_controll
	SET Date_last_inserted = @Today
	WHERE File_name = @File_name;

END
GO

--EXEC sp_configure 'show advanced options', 1;
--RECONFIGURE;
--EXEC sp_configure 'Database Mail XPs', 1;
--RECONFIGURE;

--check
--SELECT * FROM msdb.dbo.sysmail_allitems ORDER BY send_request_date DESC;

-- config for mail 
--EXEC msdb.dbo.sysmail_update_account_sp
--    @account_name = 'Eva Iablocova',
--    @mailserver_name = 'smtp.gmail.com',
--    @port = 587,
--    @enable_ssl = 1,
--    @username = 'evaiablocova@gmail.com',
--    @password = 'ggmc tfxr qxab gwui';