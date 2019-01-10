using System;
using System.Collections.Generic;
using System.Drawing;

namespace HugoBotMVC.Services
{
    static class Program
    {

        public static Settings setMain;
        public static Random randNumber = new Random();
        public static long counter = 0;

        /// <summary>
        /// The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main()
        {
            // load settings
            setMain = Settings.LoadFromFile();
            if (setMain == null)
            {
                setMain = new Settings();
                setMain.setBaseColor(Color.FromArgb(185, 220, 234));
                setMain.fntMain = new Font(FontFamily.GenericSansSerif, float.Parse("10.0"));
            }
            randNumber = new Random();
            //Application.EnableVisualStyles();
            //Application.SetCompatibleTextRenderingDefault(false);
            //Application.Run(new MainForm());
        }
    }
}