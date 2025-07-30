USE [PDFparser]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[ETL_controll]') AND type in (N'U'))
BEGIN
CREATE TABLE [dbo].[ETL_controll](
  [ETL_controll_SID] [int] IDENTITY(1,1) NOT NULL,
  [File_name] [varchar](100) NULL,
  [Date_last_inserted] [datetime] NULL,
 CONSTRAINT [PK_ETL_controll_SID] PRIMARY KEY CLUSTERED 
(
  [ETL_controll_SID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
END
GO

IF NOT EXISTS (SELECT * FROM dbo.sysobjects WHERE id = OBJECT_ID(N'[DF_ETL_controll_Date_last_inserted]') AND type = 'D')
ALTER TABLE [dbo].[ETL_controll] ADD  CONSTRAINT [DF_ETL_controll_Date_last_inserted]  DEFAULT (getdate()) FOR [Date_last_inserted]
GO

