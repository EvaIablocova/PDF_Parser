--          Adding preset values           --
---------------------------------------------------------------
;WITH PresetValues AS (
  SELECT [Recipient], [Description], [SlackWebHook], [SlackEmail], [IsEnabled]
  FROM (VALUES
     ('Eva Iablocova','Default channel to send: [eva-iablocova]','https://hooks.slack.com/services/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',  'evaiablocova@gmail.com',  1)

    --,('Recipient', 'Description', 'SlackWebHook', 'SlackEmail',  IsEnabled(0/1))
    --()
    ) AS Tbl ([Recipient], [Description], [SlackWebHook], [SlackEmail], [IsEnabled])
  )

INSERT INTO Monitor_SlackConfigSetting ([Recipient], [Description], [SlackWebHook], [SlackEmail], [IsEnabled])
SELECT 
  P.[Recipient], P.[Description], P.[SlackWebHook], P.[SlackEmail], P.[IsEnabled]
FROM PresetValues P
LEFT JOIN [Monitor_SlackConfigSetting] M ON M.Recipient = P.Recipient
WHERE M.Recipient IS NULL
GO
