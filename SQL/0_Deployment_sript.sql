USE [PDFparser]
GO
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Sediul]') AND type in (N'U'))
ALTER TABLE [dbo].[Sediul] DROP CONSTRAINT IF EXISTS [DF_Sediul_DateUpdated]
GO
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Sediul]') AND type in (N'U'))
ALTER TABLE [dbo].[Sediul] DROP CONSTRAINT IF EXISTS [DF_Sediul_DateCreated]
GO
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Sediul]') AND type in (N'U'))
ALTER TABLE [dbo].[Sediul] DROP CONSTRAINT IF EXISTS [DF_Sediul_is_deleted]
GO
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Sediul]') AND type in (N'U'))
ALTER TABLE [dbo].[Sediul] DROP CONSTRAINT IF EXISTS [DF_Sediul_error_message]
GO
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Sediul]') AND type in (N'U'))
ALTER TABLE [dbo].[Sediul] DROP CONSTRAINT IF EXISTS [DF_Sediul_is_valid]
GO
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Reducere]') AND type in (N'U'))
ALTER TABLE [dbo].[Reducere] DROP CONSTRAINT IF EXISTS [DF_Reducere_DateUpdated]
GO
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Reducere]') AND type in (N'U'))
ALTER TABLE [dbo].[Reducere] DROP CONSTRAINT IF EXISTS [DF_Reducere_DateCreated]
GO
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Reducere]') AND type in (N'U'))
ALTER TABLE [dbo].[Reducere] DROP CONSTRAINT IF EXISTS [DF_Reducere_is_deleted]
GO
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Reducere]') AND type in (N'U'))
ALTER TABLE [dbo].[Reducere] DROP CONSTRAINT IF EXISTS [DF_Reducere_error_message]
GO
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Reducere]') AND type in (N'U'))
ALTER TABLE [dbo].[Reducere] DROP CONSTRAINT IF EXISTS [DF_Reducere_is_valid]
GO
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Lichidarea]') AND type in (N'U'))
ALTER TABLE [dbo].[Lichidarea] DROP CONSTRAINT IF EXISTS [DF_Lichidarea_DateUpdated]
GO
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Lichidarea]') AND type in (N'U'))
ALTER TABLE [dbo].[Lichidarea] DROP CONSTRAINT IF EXISTS [DF_Lichidarea_DateCreated]
GO
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Lichidarea]') AND type in (N'U'))
ALTER TABLE [dbo].[Lichidarea] DROP CONSTRAINT IF EXISTS [DF_Lichidarea_is_deleted]
GO
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Lichidarea]') AND type in (N'U'))
ALTER TABLE [dbo].[Lichidarea] DROP CONSTRAINT IF EXISTS [DF_Lichidarea_error_message]
GO
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Lichidarea]') AND type in (N'U'))
ALTER TABLE [dbo].[Lichidarea] DROP CONSTRAINT IF EXISTS [DF_Lichidarea_is_valid]
GO
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Init_reorg]') AND type in (N'U'))
ALTER TABLE [dbo].[Init_reorg] DROP CONSTRAINT IF EXISTS [DF_Init_reorg_DateUpdated]
GO
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Init_reorg]') AND type in (N'U'))
ALTER TABLE [dbo].[Init_reorg] DROP CONSTRAINT IF EXISTS [DF_Init_reorg_DateCreated]
GO
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Init_reorg]') AND type in (N'U'))
ALTER TABLE [dbo].[Init_reorg] DROP CONSTRAINT IF EXISTS [DF_Init_reorg_is_deleted]
GO
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Init_reorg]') AND type in (N'U'))
ALTER TABLE [dbo].[Init_reorg] DROP CONSTRAINT IF EXISTS [DF_Init_reorg_error_message]
GO
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Init_reorg]') AND type in (N'U'))
ALTER TABLE [dbo].[Init_reorg] DROP CONSTRAINT IF EXISTS [DF_Init_reorg_is_valid]
GO
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Init_lichid]') AND type in (N'U'))
ALTER TABLE [dbo].[Init_lichid] DROP CONSTRAINT IF EXISTS [DF_Init_lichid_DateUpdated]
GO
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Init_lichid]') AND type in (N'U'))
ALTER TABLE [dbo].[Init_lichid] DROP CONSTRAINT IF EXISTS [DF_Init_lichid_DateCreated]
GO
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Init_lichid]') AND type in (N'U'))
ALTER TABLE [dbo].[Init_lichid] DROP CONSTRAINT IF EXISTS [DF_Init_lichid_is_deleted]
GO
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Init_lichid]') AND type in (N'U'))
ALTER TABLE [dbo].[Init_lichid] DROP CONSTRAINT IF EXISTS [DF_Init_lichid_error_message]
GO
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Init_lichid]') AND type in (N'U'))
ALTER TABLE [dbo].[Init_lichid] DROP CONSTRAINT IF EXISTS [DF_Init_lichid_is_valid]
GO
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Inactive]') AND type in (N'U'))
ALTER TABLE [dbo].[Inactive] DROP CONSTRAINT IF EXISTS [DF_Inactive_DateUpdated]
GO
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Inactive]') AND type in (N'U'))
ALTER TABLE [dbo].[Inactive] DROP CONSTRAINT IF EXISTS [DF_Inactive_DateCreated]
GO
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Inactive]') AND type in (N'U'))
ALTER TABLE [dbo].[Inactive] DROP CONSTRAINT IF EXISTS [DF_Inactive_is_deleted]
GO
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Inactive]') AND type in (N'U'))
ALTER TABLE [dbo].[Inactive] DROP CONSTRAINT IF EXISTS [DF_Inactive_error_message]
GO
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Inactive]') AND type in (N'U'))
ALTER TABLE [dbo].[Inactive] DROP CONSTRAINT IF EXISTS [DF_Inactive_is_valid]
GO
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Finaliz_proced_reorg]') AND type in (N'U'))
ALTER TABLE [dbo].[Finaliz_proced_reorg] DROP CONSTRAINT IF EXISTS [DF_Finaliz_proced_reorg_DateUpdated]
GO
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Finaliz_proced_reorg]') AND type in (N'U'))
ALTER TABLE [dbo].[Finaliz_proced_reorg] DROP CONSTRAINT IF EXISTS [DF_Finaliz_proced_reorg_DateCreated]
GO
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Finaliz_proced_reorg]') AND type in (N'U'))
ALTER TABLE [dbo].[Finaliz_proced_reorg] DROP CONSTRAINT IF EXISTS [DF_Finaliz_proced_reorg_is_deleted]
GO
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Finaliz_proced_reorg]') AND type in (N'U'))
ALTER TABLE [dbo].[Finaliz_proced_reorg] DROP CONSTRAINT IF EXISTS [DF_Finaliz_proced_reorg_error_message]
GO
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Finaliz_proced_reorg]') AND type in (N'U'))
ALTER TABLE [dbo].[Finaliz_proced_reorg] DROP CONSTRAINT IF EXISTS [DF_Finaliz_proced_reorg_is_valid]
GO
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Denumirea]') AND type in (N'U'))
ALTER TABLE [dbo].[Denumirea] DROP CONSTRAINT IF EXISTS [DF_Denumirea_DateUpdated]
GO
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Denumirea]') AND type in (N'U'))
ALTER TABLE [dbo].[Denumirea] DROP CONSTRAINT IF EXISTS [DF_Denumirea_DateCreated]
GO
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Denumirea]') AND type in (N'U'))
ALTER TABLE [dbo].[Denumirea] DROP CONSTRAINT IF EXISTS [DF_Denumirea_is_deleted]
GO
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Denumirea]') AND type in (N'U'))
ALTER TABLE [dbo].[Denumirea] DROP CONSTRAINT IF EXISTS [DF_Denumirea_error_message]
GO
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Denumirea]') AND type in (N'U'))
ALTER TABLE [dbo].[Denumirea] DROP CONSTRAINT IF EXISTS [DF_Denumirea_is_valid]
GO
DROP TABLE IF EXISTS [dbo].[staging_Sediul]
GO
DROP TABLE IF EXISTS [dbo].[staging_Reducere]
GO
DROP TABLE IF EXISTS [dbo].[staging_Lichidarea]
GO
DROP TABLE IF EXISTS [dbo].[staging_Init_reorg]
GO
DROP TABLE IF EXISTS [dbo].[staging_Init_lichid]
GO
DROP TABLE IF EXISTS [dbo].[staging_Inactive]
GO
DROP TABLE IF EXISTS [dbo].[staging_Finaliz_proced_reorg]
GO
DROP TABLE IF EXISTS [dbo].[staging_Denumirea]
GO
DROP TABLE IF EXISTS [dbo].[Sediul]
GO
DROP TABLE IF EXISTS [dbo].[Reducere]
GO
DROP TABLE IF EXISTS [dbo].[Lichidarea]
GO
DROP TABLE IF EXISTS [dbo].[Init_reorg]
GO
DROP TABLE IF EXISTS [dbo].[Init_lichid]
GO
DROP TABLE IF EXISTS [dbo].[Inactive]
GO
DROP TABLE IF EXISTS [dbo].[Finaliz_proced_reorg]
GO
DROP TABLE IF EXISTS [dbo].[Denumirea]
GO
DROP TABLE IF EXISTS [dbo].[Logs]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Denumirea](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[No] [nvarchar](255) NULL,
	[Date_of_announcement] [nvarchar](255) NULL,
	[IDNO] [nvarchar](255) NULL,
	[Name] [nvarchar](255) NULL,
	[Address] [nvarchar](255) NULL,
	[Name_From] [nvarchar](255) NULL,
	[Name_Into] [nvarchar](255) NULL,
	[is_valid] [bit] NULL,
	[error_message] [varchar](255) NULL,
	[is_deleted] [bit] NULL,
	[DateCreated] [datetime] NULL,
	[DateUpdated] [datetime] NULL,
 CONSTRAINT [PK_Denumirea] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Finaliz_proced_reorg](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[No] [nvarchar](255) NULL,
	[Date_of_announcement] [nvarchar](255) NULL,
	[IDNO] [nvarchar](255) NULL,
	[Name] [nvarchar](255) NULL,
	[Type_of_reorganization] [nvarchar](255) NULL,
	[Successors_of_rights] [nvarchar](255) NULL,
	[is_valid] [bit] NULL,
	[error_message] [varchar](255) NULL,
	[is_deleted] [bit] NULL,
	[DateCreated] [datetime] NULL,
	[DateUpdated] [datetime] NULL,
 CONSTRAINT [PK_Finaliz_proced_reorg] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Inactive](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[No] [nvarchar](255) NULL,
	[Date_of_announcement] [nvarchar](255) NULL,
	[IDNO] [nvarchar](255) NULL,
	[Name] [nvarchar](255) NULL,
	[Address] [nvarchar](255) NULL,
	[Date_of_dissolution] [nvarchar](255) NULL,
	[is_valid] [bit] NULL,
	[error_message] [varchar](255) NULL,
	[is_deleted] [bit] NULL,
	[DateCreated] [datetime] NULL,
	[DateUpdated] [datetime] NULL,
 CONSTRAINT [PK_Inactive] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Init_lichid](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[No] [nvarchar](255) NULL,
	[Date_of_announcement] [nvarchar](255) NULL,
	[IDNO] [nvarchar](255) NULL,
	[Name] [nvarchar](255) NULL,
	[Address] [nvarchar](255) NULL,
	[is_valid] [bit] NULL,
	[error_message] [varchar](255) NULL,
	[is_deleted] [bit] NULL,
	[DateCreated] [datetime] NULL,
	[DateUpdated] [datetime] NULL,
 CONSTRAINT [PK_Init_lichid] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Init_reorg](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[No] [nvarchar](255) NULL,
	[Date_of_announcement] [nvarchar](255) NULL,
	[IDNO] [nvarchar](255) NULL,
	[Name] [nvarchar](255) NULL,
	[Type_of_reorganization_1] [nvarchar](255) NULL,
	[Type_of_reorganization_2] [nvarchar](255) NULL,
	[Address] [nvarchar](255) NULL,
	[is_valid] [bit] NULL,
	[error_message] [varchar](255) NULL,
	[is_deleted] [bit] NULL,
	[DateCreated] [datetime] NULL,
	[DateUpdated] [datetime] NULL,
 CONSTRAINT [PK_Init_reorg] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Lichidarea](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[No] [nvarchar](255) NULL,
	[Date_of_announcement] [nvarchar](255) NULL,
	[IDNO] [nvarchar](255) NULL,
	[Name] [nvarchar](255) NULL,
	[Address] [nvarchar](255) NULL,
	[Date_of_deregistretion] [nvarchar](255) NULL,
	[is_valid] [bit] NULL,
	[error_message] [varchar](255) NULL,
	[is_deleted] [bit] NULL,
	[DateCreated] [datetime] NULL,
	[DateUpdated] [datetime] NULL,
 CONSTRAINT [PK_Lichidarea] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Reducere](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[No] [nvarchar](255) NULL,
	[Date_of_announcement] [nvarchar](255) NULL,
	[IDNO] [nvarchar](255) NULL,
	[Name] [nvarchar](255) NULL,
	[Address] [nvarchar](255) NULL,
	[Price_From] [nvarchar](255) NULL,
	[Price_Into] [nvarchar](255) NULL,
	[is_valid] [bit] NULL,
	[error_message] [varchar](255) NULL,
	[is_deleted] [bit] NULL,
	[DateCreated] [datetime] NULL,
	[DateUpdated] [datetime] NULL,
 CONSTRAINT [PK_Reducere] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Sediul](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[No] [nvarchar](255) NULL,
	[Date_of_announcement] [nvarchar](255) NULL,
	[IDNO] [nvarchar](255) NULL,
	[Name] [nvarchar](255) NULL,
	[Address] [nvarchar](255) NULL,
	[Address_From] [nvarchar](255) NULL,
	[Address_Into] [nvarchar](255) NULL,
	[is_valid] [bit] NULL,
	[error_message] [varchar](255) NULL,
	[is_deleted] [bit] NULL,
	[DateCreated] [datetime] NULL,
	[DateUpdated] [datetime] NULL,
 CONSTRAINT [PK_Sediul] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[staging_Denumirea](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[No] [nvarchar](255) NULL,
	[Date_of_announcement] [nvarchar](255) NULL,
	[IDNO] [nvarchar](255) NULL,
	[Name] [nvarchar](255) NULL,
	[Address] [nvarchar](255) NULL,
	[Name_From] [nvarchar](255) NULL,
	[Name_Into] [nvarchar](255) NULL,
	[DateCreated] [datetime] NULL
 CONSTRAINT [PK_staging_Denumirea] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[staging_Finaliz_proced_reorg](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[No] [nvarchar](255) NULL,
	[Date_of_announcement] [nvarchar](255) NULL,
	[IDNO] [nvarchar](255) NULL,
	[Name] [nvarchar](255) NULL,
	[Type_of_reorganization] [nvarchar](255) NULL,
	[Successors_of_rights] [nvarchar](255) NULL,
	[DateCreated] [datetime] NULL
 CONSTRAINT [PK_staging_Finaliz_proced_reorg] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[staging_Inactive](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[No] [nvarchar](255) NULL,
	[Date_of_announcement] [nvarchar](255) NULL,
	[IDNO] [nvarchar](255) NULL,
	[Name] [nvarchar](255) NULL,
	[Address] [nvarchar](255) NULL,
	[Date_of_dissolution] [nvarchar](255) NULL,
	[DateCreated] [datetime] NULL
 CONSTRAINT [PK_staging_Inactive] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[staging_Init_lichid](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[No] [nvarchar](255) NULL,
	[Date_of_announcement] [nvarchar](255) NULL,
	[IDNO] [nvarchar](255) NULL,
	[Name] [nvarchar](255) NULL,
	[Address] [nvarchar](255) NULL,
	[DateCreated] [datetime] NULL
 CONSTRAINT [PK_staging_Init_lichid] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[staging_Init_reorg](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[No] [nvarchar](255) NULL,
	[Date_of_announcement] [nvarchar](255) NULL,
	[IDNO] [nvarchar](255) NULL,
	[Name] [nvarchar](255) NULL,
	[Type_of_reorganization_1] [nvarchar](255) NULL,
	[Type_of_reorganization_2] [nvarchar](255) NULL,
	[Address] [nvarchar](255) NULL,
	[DateCreated] [datetime] NULL
 CONSTRAINT [PK_staging_Init_reorg] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[staging_Lichidarea](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[No] [nvarchar](255) NULL,
	[Date_of_announcement] [nvarchar](255) NULL,
	[IDNO] [nvarchar](255) NULL,
	[Name] [nvarchar](255) NULL,
	[Address] [nvarchar](255) NULL,
	[Date_of_deregistretion] [nvarchar](255) NULL,
	[DateCreated] [datetime] NULL
 CONSTRAINT [PK_staging_Lichidarea] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[staging_Reducere](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[No] [nvarchar](255) NULL,
	[Date_of_announcement] [nvarchar](255) NULL,
	[IDNO] [nvarchar](255) NULL,
	[Name] [nvarchar](255) NULL,
	[Address] [nvarchar](255) NULL,
	[Price_From] [nvarchar](255) NULL,
	[Price_Into] [nvarchar](255) NULL,
	[DateCreated] [datetime] NULL
 CONSTRAINT [PK_staging_Reducere] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[staging_Sediul](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[No] [nvarchar](255) NULL,
	[Date_of_announcement] [nvarchar](255) NULL,
	[IDNO] [nvarchar](255) NULL,
	[Name] [nvarchar](255) NULL,
	[Address] [nvarchar](255) NULL,
	[Address_From] [nvarchar](255) NULL,
	[Address_Into] [nvarchar](255) NULL,
	[DateCreated] [datetime] NULL
 CONSTRAINT [PK_staging_Sediul] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
CREATE TABLE [dbo].[Logs] (
    [ID] BIGINT IDENTITY(1,1) NOT NULL,
    [DateInserted] DATETIME NOT NULL,
    [ExecutionStep] VARCHAR(50) NOT NULL,
    [MessageDescription] VARCHAR(2000) NULL,

    CONSTRAINT [PK_Logs] PRIMARY KEY CLUSTERED ([ID] ASC)
        WITH (
            PAD_INDEX = OFF,
            STATISTICS_NORECOMPUTE = OFF,
            IGNORE_DUP_KEY = OFF,
            ALLOW_ROW_LOCKS = ON,
            ALLOW_PAGE_LOCKS = ON,
            OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF
        ) ON [PRIMARY],

    CONSTRAINT [CK_Logs_ExecutionStep] CHECK (
        [ExecutionStep] IN (
            'Py.Loader',
            'Py.Parser',
            'Py.Staging',
            'SQL MERGE',
            'SQL Validator',
			'SQL INFO status'
        )
    )
) ON [PRIMARY];
GO
ALTER TABLE [dbo].[Denumirea] ADD  CONSTRAINT [DF_Denumirea_error_message]  DEFAULT ('') FOR [error_message]
GO
ALTER TABLE [dbo].[Denumirea] ADD  CONSTRAINT [DF_Denumirea_is_deleted]  DEFAULT ((0)) FOR [is_deleted]
GO
ALTER TABLE [dbo].[Denumirea] ADD  CONSTRAINT [DF_Denumirea_DateCreated]  DEFAULT (getdate()) FOR [DateCreated]
GO
ALTER TABLE [dbo].[Denumirea] ADD  CONSTRAINT [DF_Denumirea_DateUpdated]  DEFAULT (getdate()) FOR [DateUpdated]
GO
ALTER TABLE [dbo].[Finaliz_proced_reorg] ADD  CONSTRAINT [DF_Finaliz_proced_reorg_error_message]  DEFAULT ('') FOR [error_message]
GO
ALTER TABLE [dbo].[Finaliz_proced_reorg] ADD  CONSTRAINT [DF_Finaliz_proced_reorg_is_deleted]  DEFAULT ((0)) FOR [is_deleted]
GO
ALTER TABLE [dbo].[Finaliz_proced_reorg] ADD  CONSTRAINT [DF_Finaliz_proced_reorg_DateCreated]  DEFAULT (getdate()) FOR [DateCreated]
GO
ALTER TABLE [dbo].[Finaliz_proced_reorg] ADD  CONSTRAINT [DF_Finaliz_proced_reorg_DateUpdated]  DEFAULT (getdate()) FOR [DateUpdated]
GO
ALTER TABLE [dbo].[Inactive] ADD  CONSTRAINT [DF_Inactive_error_message]  DEFAULT ('') FOR [error_message]
GO
ALTER TABLE [dbo].[Inactive] ADD  CONSTRAINT [DF_Inactive_is_deleted]  DEFAULT ((0)) FOR [is_deleted]
GO
ALTER TABLE [dbo].[Inactive] ADD  CONSTRAINT [DF_Inactive_DateCreated]  DEFAULT (getdate()) FOR [DateCreated]
GO
ALTER TABLE [dbo].[Inactive] ADD  CONSTRAINT [DF_Inactive_DateUpdated]  DEFAULT (getdate()) FOR [DateUpdated]
GO
ALTER TABLE [dbo].[Init_lichid] ADD  CONSTRAINT [DF_Init_lichid_error_message]  DEFAULT ('') FOR [error_message]
GO
ALTER TABLE [dbo].[Init_lichid] ADD  CONSTRAINT [DF_Init_lichid_is_deleted]  DEFAULT ((0)) FOR [is_deleted]
GO
ALTER TABLE [dbo].[Init_lichid] ADD  CONSTRAINT [DF_Init_lichid_DateCreated]  DEFAULT (getdate()) FOR [DateCreated]
GO
ALTER TABLE [dbo].[Init_lichid] ADD  CONSTRAINT [DF_Init_lichid_DateUpdated]  DEFAULT (getdate()) FOR [DateUpdated]
GO
ALTER TABLE [dbo].[Init_reorg] ADD  CONSTRAINT [DF_Init_reorg_error_message]  DEFAULT ('') FOR [error_message]
GO
ALTER TABLE [dbo].[Init_reorg] ADD  CONSTRAINT [DF_Init_reorg_is_deleted]  DEFAULT ((0)) FOR [is_deleted]
GO
ALTER TABLE [dbo].[Init_reorg] ADD  CONSTRAINT [DF_Init_reorg_DateCreated]  DEFAULT (getdate()) FOR [DateCreated]
GO
ALTER TABLE [dbo].[Init_reorg] ADD  CONSTRAINT [DF_Init_reorg_DateUpdated]  DEFAULT (getdate()) FOR [DateUpdated]
GO
ALTER TABLE [dbo].[Lichidarea] ADD  CONSTRAINT [DF_Lichidarea_error_message]  DEFAULT ('') FOR [error_message]
GO
ALTER TABLE [dbo].[Lichidarea] ADD  CONSTRAINT [DF_Lichidarea_is_deleted]  DEFAULT ((0)) FOR [is_deleted]
GO
ALTER TABLE [dbo].[Lichidarea] ADD  CONSTRAINT [DF_Lichidarea_DateCreated]  DEFAULT (getdate()) FOR [DateCreated]
GO
ALTER TABLE [dbo].[Lichidarea] ADD  CONSTRAINT [DF_Lichidarea_DateUpdated]  DEFAULT (getdate()) FOR [DateUpdated]
GO
ALTER TABLE [dbo].[Reducere] ADD  CONSTRAINT [DF_Reducere_error_message]  DEFAULT ('') FOR [error_message]
GO
ALTER TABLE [dbo].[Reducere] ADD  CONSTRAINT [DF_Reducere_is_deleted]  DEFAULT ((0)) FOR [is_deleted]
GO
ALTER TABLE [dbo].[Reducere] ADD  CONSTRAINT [DF_Reducere_DateCreated]  DEFAULT (getdate()) FOR [DateCreated]
GO
ALTER TABLE [dbo].[Reducere] ADD  CONSTRAINT [DF_Reducere_DateUpdated]  DEFAULT (getdate()) FOR [DateUpdated]
GO
ALTER TABLE [dbo].[Sediul] ADD  CONSTRAINT [DF_Sediul_error_message]  DEFAULT ('') FOR [error_message]
GO
ALTER TABLE [dbo].[Sediul] ADD  CONSTRAINT [DF_Sediul_is_deleted]  DEFAULT ((0)) FOR [is_deleted]
GO
ALTER TABLE [dbo].[Sediul] ADD  CONSTRAINT [DF_Sediul_DateCreated]  DEFAULT (getdate()) FOR [DateCreated]
GO
ALTER TABLE [dbo].[Sediul] ADD  CONSTRAINT [DF_Sediul_DateUpdated]  DEFAULT (getdate()) FOR [DateUpdated]
GO
ALTER TABLE [dbo].[Logs] ADD  CONSTRAINT [DF_Logs_ExecutionStep]  DEFAULT ('SQL INFO status') FOR [ExecutionStep]
GO
ALTER TABLE [dbo].[Logs] ADD  CONSTRAINT [DF_Logs_DateInserted]  DEFAULT (getdate()) FOR [DateInserted]
GO
ALTER TABLE [dbo].[Logs] ADD  CONSTRAINT [DF_Logs_MessageDescription]  DEFAULT ('') FOR [MessageDescription]
GO
ALTER TABLE [dbo].[staging_Sediul] ADD  CONSTRAINT [DF_staging_Sediul_DateCreated]  DEFAULT (getdate()) FOR [DateCreated]
GO
ALTER TABLE [dbo].[staging_Reducere] ADD  CONSTRAINT [DF_staging_Reducere_DateCreated]  DEFAULT (getdate()) FOR [DateCreated]
GO
ALTER TABLE [dbo].[staging_Lichidarea] ADD  CONSTRAINT [DF_staging_Lichidarea_DateCreated]  DEFAULT (getdate()) FOR [DateCreated]
GO
ALTER TABLE [dbo].[staging_Init_reorg] ADD  CONSTRAINT [DF_staging_Init_reorg_DateCreated]  DEFAULT (getdate()) FOR [DateCreated]
GO
ALTER TABLE [dbo].[staging_Init_lichid] ADD  CONSTRAINT [DF_staging_Init_lichid_DateCreated]  DEFAULT (getdate()) FOR [DateCreated]
GO
ALTER TABLE [dbo].[staging_Inactive] ADD  CONSTRAINT [DF_staging_Inactive_DateCreated]  DEFAULT (getdate()) FOR [DateCreated]
GO
ALTER TABLE [dbo].[staging_Finaliz_proced_reorg] ADD  CONSTRAINT [DF_staging_Finaliz_proced_reorg_DateCreated]  DEFAULT (getdate()) FOR [DateCreated]
GO
ALTER TABLE [dbo].[staging_Denumirea] ADD  CONSTRAINT [DF_staging_Denumirea_DateCreated]  DEFAULT (getdate()) FOR [DateCreated]
GO

