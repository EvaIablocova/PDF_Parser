SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Monitor_SlackConfigSetting]') AND type in (N'U'))
BEGIN
CREATE TABLE [dbo].[Monitor_SlackConfigSetting](
  [SlackConfigSetting_SID] [int] IDENTITY(1,1) NOT NULL,
  [Recipient] [varchar](100) NULL,
  [Description] [varchar](200) NULL,
  [SlackWebHook] [varchar](200) NULL,
  [SlackEmail] [varchar](200) NULL,
  [DateCreated] [datetime] NOT NULL,
  [isEnabled] [bit] NOT NULL,
 CONSTRAINT [PK_Monitor_SlackConfigSetting] PRIMARY KEY CLUSTERED 
(
  [SlackConfigSetting_SID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
END
GO

IF NOT EXISTS (SELECT * FROM dbo.sysobjects WHERE id = OBJECT_ID(N'[DF_Monitor_SlackConfigSetting_DateCreated]') AND type = 'D')
ALTER TABLE [dbo].[Monitor_SlackConfigSetting] ADD  CONSTRAINT [DF_Monitor_SlackConfigSetting_DateCreated]  DEFAULT (getdate()) FOR [DateCreated]
GO

IF NOT EXISTS (SELECT * FROM dbo.sysobjects WHERE id = OBJECT_ID(N'[DF_Monitor_SlackConfigSetting_IsEnabled]') AND type = 'D')
ALTER TABLE [dbo].[Monitor_SlackConfigSetting] ADD  CONSTRAINT [DF_Monitor_SlackConfigSetting_IsEnabled]  DEFAULT ((0)) FOR [isEnabled]
GO
