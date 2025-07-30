--          Adding preset values           --
---------------------------------------------------------------
;WITH PresetValues AS (
  SELECT [File_name], [Date_last_inserted]
  FROM (VALUES
     ('Denumirea', '1900-01-01'),
	 ('Finaliz_proced_reorg', '1900-01-01'),
	 ('Inactive', '1900-01-01'),
	 ('Init_lichid', '1900-01-01'),
	 ('Init_reorg', '1900-01-01'),
	 ('Lichidarea', '1900-01-01'),
	 ('Reducere', '1900-01-01'),
	 ('Sediul', '1900-01-01')

    --,('Recipient', 'Description', 'SlackWebHook', 'SlackEmail',  IsEnabled(0/1))
    --()
    ) AS Tbl ([File_name], [Date_last_inserted])
  )

INSERT INTO ETL_controll ([File_name], [Date_last_inserted])
SELECT 
  P.[File_name], P.[Date_last_inserted]
FROM PresetValues P
LEFT JOIN [ETL_controll] E ON E.File_name = P.File_name
WHERE E.File_name IS NULL
GO
