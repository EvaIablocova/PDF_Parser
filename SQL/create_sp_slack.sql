SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
/*===================================================================================================================
 Stored Procedure  : dbo.Monitor_SendSlackMessage

 Purpose      : Send Messages to Slack Channels
 Input Parameters  : @Recipient, @Message

 Output Parameters  : None

 Usage        : EXEC [EnterpriseDW].dbo.Monitor_SendSlackMessage 'bi_team_monsato','some_message'

=====================================================================================================================*/
CREATE OR ALTER PROCEDURE [dbo].[Monitor_SendSlackMessage]
  @Recipient VARCHAR(100) = NULL,
  @Message VARCHAR(5000) = NULL
AS
BEGIN
  
  DECLARE 
    @WebHook VARCHAR(500),
    @ServerName VARCHAR (100),
    @SlackMessage VARCHAR(8000) = 'curl -k -X POST -H "Content-type:application/json" --data "{''text'':''#Replace#''}" #WebHook#'
  
  SELECT TOP 1 @WebHook = SlackWebHook
  FROM Monitor_SlackConfigSetting S
  JOIN (VALUES 
        -- if there is [WARNING] keyword in a message we try find/sent to that specific channel --
        (4,IIF(CHARINDEX('[INFO]',@message) > 0,'INFO_'+ @Recipient,'')), 
        (3,IIF(CHARINDEX('[WARNING]',@message) > 0,'WARNING_'+ @Recipient,'')), 
        (2,@Recipient),
        (1,'Default')
     ) AS Tab(Id,Name) ON Tab.Name = S.Recipient
  ORDER BY Tab.Id DESC

  IF @WebHook IS NULL
    THROW 51000,'Unknown Slack Recipient',1;
    
  IF ((@Recipient IS NULL) OR (@Message IS NULL))
    THROW 51000, 'Warning: Fill in both params <Recipient> and <Message>!!!',1;
  
  SET @ServerName = REPLACE(@@SERVERNAME,'\','\\') + FORMAT(GETDATE(),' `MMM dd yyyy hh:mm:ss tt`');
  SET @Message = REPLACE(@Message,'\','\\')
  SET @Message = REPLACE(@Message,'\\n','\n')
  SET @Message = REPLACE(@Message,'''','\''');
  SET @SlackMessage = REPLACE(@SlackMessage,'#Replace#', @Message)
  SET @SlackMessage = REPLACE(@SlackMessage,'#ServerName#',' \n`ServerName:`' + @ServerName)
  SET @SlackMessage = REPLACE(@SlackMessage,'#WebHook#',@WebHook)
        
  EXEC xp_cmdshell @SlackMessage

END
GO

--EXEC sp_configure 'show advanced options', 1;
--RECONFIGURE;
--EXEC sp_configure 'xp_cmdshell', 1;
--RECONFIGURE;

--EXEC [ASPdb15].dbo.Monitor_SendSlackMessage 'Eva Iablocova','test message'