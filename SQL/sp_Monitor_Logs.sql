USE [PDFparser];
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
/*===================================================================================================================
 Stored Procedure  : dbo.Monitor_Logs

Purpose: Send messages to Slack channels if:
													1) No files have been identified to be loaded.
													2) An error occurred during the daily parsing process.
 
 Input Parameters  : None

 Output Parameters  : None

 Usage        : EXEC [PDFparser].dbo.Monitor_Logs 

=====================================================================================================================*/
CREATE OR ALTER PROCEDURE [dbo].[Monitor_Logs]
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @LastStartedID INT;
    DECLARE @Message NVARCHAR(500) = NULL;

    -- Find the last "Started time:%" log entry
    SELECT TOP 1 @LastStartedID = [ID]
    FROM [dbo].[Logs]
    WHERE [MessageDescription] LIKE 'Started time:%'
    ORDER BY [ID] DESC;

    IF @LastStartedID IS NULL
        RETURN;

    -- Check if there is a "Finished time:%" after last start
    IF NOT EXISTS (
        SELECT 1
        FROM [dbo].[Logs]
        WHERE [ID] > @LastStartedID
          AND [MessageDescription] LIKE 'Finished time:%'
    )
    BEGIN
        SET @Message = 'An error occurred during daily parsing process';
    END
    ELSE
    BEGIN
        -- Check for "Identified 0 files to be loaded%" after last start
        IF EXISTS (
            SELECT 1
            FROM [dbo].[Logs]
            WHERE [ID] > @LastStartedID
              AND [MessageDescription] LIKE 'Identified 0 files to be loaded%'
        )
        BEGIN
            SET @Message = 'No changings in dates in site';
        END
        -- If "Identified % files to be loaded%" (not 0), do nothing (no message)
    END

    IF @Message IS NOT NULL
    BEGIN
        EXEC [PDFparser].dbo.Monitor_SendSlackMessage 'Eva Iablocova', @Message;
    END
END
GO