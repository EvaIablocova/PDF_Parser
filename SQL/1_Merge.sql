  USE [PDFparser]
  GO

  INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
  VALUES ('SQL MERGE', 'Denumirea [start]')
  GO

  INSERT INTO [Denumirea] ([No], [Date_of_announcement],[IDNO],[Name],[Address],[Name_From],[Name_Into])
  SELECT [No], [Date_of_announcement],[IDNO],[Name],[Address],[Name_From],[Name_Into] FROM [staging_Denumirea]
  EXCEPT
  SELECT [No], [Date_of_announcement],[IDNO],[Name],[Address],[Name_From],[Name_Into] FROM [Denumirea]
  GO

  INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
  VALUES ('SQL MERGE', 'Denumirea [done]')
  GO

  INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
  VALUES ('SQL MERGE', 'Finaliz_proced_reorg [start]')
  GO

  INSERT INTO [Finaliz_proced_reorg] ([No], [Date_of_announcement],[IDNO],[Name],[Type_of_reorganization],[Successors_of_rights])
  SELECT [No], [Date_of_announcement],[IDNO],[Name],[Type_of_reorganization],[Successors_of_rights] FROM [staging_Finaliz_proced_reorg]
  EXCEPT
  SELECT [No], [Date_of_announcement],[IDNO],[Name],[Type_of_reorganization],[Successors_of_rights] FROM [Finaliz_proced_reorg]
  
  INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
  VALUES ('SQL MERGE', 'Finaliz_proced_reorg [done]')
  GO

  INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
  VALUES ('SQL MERGE', 'Inactive [start]')
  GO

  INSERT INTO [Inactive] ([No], [Date_of_announcement],[IDNO],[Name],[Address],[Date_of_dissolution])
  SELECT [No], [Date_of_announcement],[IDNO],[Name],[Address],[Date_of_dissolution] FROM [staging_Inactive]
  EXCEPT
  SELECT [No], [Date_of_announcement],[IDNO],[Name],[Address],[Date_of_dissolution] FROM [Inactive]


  INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
  VALUES ('SQL MERGE', 'Inactive [done]')
  GO

  INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
  VALUES ('SQL MERGE', 'Init_lichid [start]')
  GO

  INSERT INTO [Init_lichid] ([No], [Date_of_announcement],[IDNO],[Name],[Address])
  SELECT [No], [Date_of_announcement],[IDNO],[Name],[Address] FROM [staging_Init_lichid]
  EXCEPT
  SELECT [No], [Date_of_announcement],[IDNO],[Name],[Address] FROM [Init_lichid]
  

  INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
  VALUES ('SQL MERGE', 'Init_lichid [done]')
  GO

  INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
  VALUES ('SQL MERGE', 'Init_reorg [start]')
  GO

  INSERT INTO [Init_reorg] ([No], [Date_of_announcement],[IDNO],[Name],[Type_of_reorganization_1],[Type_of_reorganization_2],[Address])
  SELECT [No], [Date_of_announcement],[IDNO],[Name],[Type_of_reorganization_1],[Type_of_reorganization_2],[Address] FROM [staging_Init_reorg]
  EXCEPT
  SELECT [No], [Date_of_announcement],[IDNO],[Name],[Type_of_reorganization_1],[Type_of_reorganization_2],[Address] FROM [Init_reorg]
  

  INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
  VALUES ('SQL MERGE', 'Init_reorg [done]')
  GO

  INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
  VALUES ('SQL MERGE', 'Lichidarea [start]')
  GO

  INSERT INTO [Lichidarea] ([No], [Date_of_announcement],[IDNO],[Name],[Address],[Date_of_deregistretion])
  SELECT [No], [Date_of_announcement],[IDNO],[Name],[Address],[Date_of_deregistretion] FROM [staging_Lichidarea]
  EXCEPT
  SELECT [No], [Date_of_announcement],[IDNO],[Name],[Address],[Date_of_deregistretion] FROM [Lichidarea]


  INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
  VALUES ('SQL MERGE', 'Lichidarea [done]')
  GO

  INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
  VALUES ('SQL MERGE', 'Reducere [start]')
  GO

  INSERT INTO [Reducere] ([No], [Date_of_announcement], [IDNO], [Name], [Address], [Price_From], [Price_Into])
  SELECT [No], [Date_of_announcement], [IDNO], [Name], [Address], [Price_From], [Price_Into]
  FROM [staging_Reducere]
  EXCEPT
  SELECT [No], [Date_of_announcement], [IDNO], [Name], [Address], [Price_From], [Price_Into]
  FROM [Reducere]

  INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
  VALUES ('SQL MERGE', 'Reducere [done]')
  GO

  INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
  VALUES ('SQL MERGE', 'Date_of_announcement [start]')
  GO

  INSERT INTO [Sediul] ([No], [Date_of_announcement],[IDNO],[Name],[Address],[Address_From],[Address_Into])
  SELECT [No], [Date_of_announcement],[IDNO],[Name],[Address],[Address_From],[Address_Into] FROM [staging_Sediul]
  EXCEPT
  SELECT [No], [Date_of_announcement],[IDNO],[Name],[Address],[Address_From],[Address_Into] FROM [Sediul]


  INSERT INTO [dbo].[Logs] ([ExecutionStep], [MessageDescription])
  VALUES ('SQL MERGE', 'Date_of_announcement [done]')
  GO