using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace HugoBotMVC.Services
{
    public static class Const
    {

        #region ColorsDefinitions
        public static System.Drawing.Color COLOR_BTN_BACK_ON = System.Drawing.Color.FromArgb(131, 192, 237);
        public static System.Drawing.Color COLOR_LEVEL_BACK = System.Drawing.Color.FromArgb(125, 198, 239);
        public static System.Drawing.Color COLOR_BTN_BACK_OFF = System.Drawing.Color.FromArgb(212, 212, 212);
        public static System.Drawing.Color COLOR_BACK = System.Drawing.Color.FromArgb(185, 220, 234);
        public static System.Drawing.Color COLOR_HEADER_BACK = System.Drawing.Color.FromArgb(131, 199, 224);
        #endregion ColorsDefinitions

        #region Files
        public static string STR_INDEX_FILE_NAME = "Index.xml";
        public static string STR_SETTINGS_FILE = "Settings.ini";
        public static string STR_FILENAME_ATTRIBUTE = "FileName";
        #endregion Files

        #region LegoXmlTags
        public static string STR_INSTANCE_TAG = "Ins";
        public static string STR_TIRP_TAG = "TIRP";
        #endregion LegoXmlTags

        #region ProgramDefinitions
        public static int INT_GRAPH_COUNT_LIMIT = 6;
        public static int INT_INSTANCE_LENGTH_CHARS = 50;
        #endregion ProgramDefinitions

        #region Interface Strings

        public static string STR_SHOW_GRAPH_FORM_MENU = "Show graph window";
        public static string STR_HIDE_GRAPH_FORM_MENU = "Hide graph window";

        #endregion


        #region DiagramDefinitions

        public static int INT_DIAGRAM_PROPERTY_WIDTH = 100;
        public static int INT_DIAGRAM_PROPERTY_HEIGHT = 50;
        public static int INT_DIAGRAM_LEVEL_SPACE = 8;
        public static int INT_DIAGRAM_LINK_WIDTH = 4;
        public static int INT_DIAGRAM_LEVELS_SPACE = 200;

        public static System.Drawing.Color COLOR_DIAGRAM_NODE_BACK = System.Drawing.Color.FromArgb(125, 198, 239);
        public static System.Drawing.Color COLOR_DIAGRAM_NODE_BORDER = System.Drawing.Color.FromArgb(211, 231, 243);
        public static System.Drawing.Color COLOR_DIAGRAM_NODE_TEXT = System.Drawing.Color.FromArgb(246, 246, 246);
        public static System.Drawing.Color COLOR_DIAGRAM_NODE_SELECTED = System.Drawing.Color.FromArgb(222, 222, 222);
        public static System.Drawing.Color COLOR_DIAGRAM_BACK = System.Drawing.Color.FromArgb(211, 231, 243);
        public static System.Drawing.Color COLOR_DIAGRAM_LINK = System.Drawing.Color.FromArgb(131, 202, 232);
        public static System.Drawing.Color COLOR_DIAGRAM_SELECTED_PATH = System.Drawing.Color.FromArgb(151, 212, 232);



        #endregion DiagramDefinitions

        #region  BinsDefinitionsTable
        public static string STR_TEMPORAL_PROPERTY_ID = "TemporalPropertyID";
        public static string STR_TEMPORAL_PROPERTY_NAME = "TemporalPropertyName";
        public static string STR_BINS_DEFINITIONS_TABLE = "BinsDefinitions";
        public static string STR_METHOD_NAME = "MethodName";
        public static string STR_METHOD_ID = "MethodID";
        public static string STR_RESULTS_ERROR1 = "Error1";
        public static string STR_RESULTS_ENTROPY = "Entropy";
        public static string STR_STATE_ID = "StateID";
        public static string STR_BIN_ID = "BinID";
        public static string[] STR_ARR_BIN_BASE_LABELS = { "Low", "Medium", "High" };
        public static string STR_BIN_LABEL = "BinLabel";
        public static string STR_BIN_FROM = "BinFrom";
        public static string STR_BIN_TO = "BinTo";

        #endregion BinsDefinitionsTable

        #region Tables Columns
        public static string STR_ENTITY_ID = "EntityID";
        #endregion

    }

}