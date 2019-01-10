using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Text;
using System.Drawing;
using System.IO;

namespace HugoBotMVC.Services
{
    class Settings
    {
        public Color colBase;
        public Color colLabels;
        public Color colHeaders;
        public Color colStatus;
        public Color colNextLevel;
        public Color colNoNextLevel;
        public Color colUnLoaded;
        public Font fntMain;


        public void setBaseColor(Color cBase)
        {
            colBase = cBase;
            colLabels = Color.FromArgb((int)(cBase.R - 0.15 * cBase.R),
                                     (int)(cBase.G - 0.15 * cBase.G),
                                     (int)(cBase.B - 0.15 * cBase.B));

            colHeaders = Color.FromArgb((int)(cBase.R - 0.1 * cBase.R),
                                   (int)(cBase.G - 0.1 * cBase.G),
                                   (int)(cBase.B - 0.1 * cBase.B));

            colStatus = Color.FromArgb((int)(cBase.R - 0.3 * cBase.R),
                                     (int)(cBase.G - 0.3 * cBase.G),
                                     (int)(cBase.B - 0.3 * cBase.B));

            colNextLevel = Color.FromArgb((int)(cBase.R - 0.2 * cBase.R),
                                          (int)(cBase.G - 0.2 * cBase.G),
                                          (int)(cBase.B - 0.2 * cBase.B));

            colNoNextLevel = Color.FromArgb(255, 255, 255);

            colUnLoaded = Color.FromArgb((int)(cBase.R - 0.1 * cBase.R),
                                          (int)(cBase.G - 0.1 * cBase.G),
                                          (int)(cBase.B - 0.1 * cBase.B));

        } // setBaseColor

        public Color getBaseColor()
        {
            return colBase;
        }

        /// <summary>
        /// loads settings from the expected settings wekamatrixfile in the same folder as the executable's
        /// </summary>
        /// <returns>new settings object</returns>
        public static Settings LoadFromFile()
        {
            string filename = "";//Methods.getFileNamePath(System.Windows.Forms.Application.ExecutablePath) + "\\" + Const.STR_SETTINGS_FILE;
            if (System.IO.File.Exists(filename))
            {
                string line, fontname, fontsize;
                string[] vals;
                Settings set = new Settings();
                using (StreamReader sr = new StreamReader(filename))
                {
                    // read base color
                    line = sr.ReadLine();
                    vals = line.Split('=');
                    vals = vals[1].Split(',');
                    set.setBaseColor(Color.FromArgb(int.Parse(vals[0]), int.Parse(vals[1]), int.Parse(vals[2])));

                    // read font name
                    line = sr.ReadLine();
                    vals = line.Split('=');
                    fontname = vals[1];
                    line = sr.ReadLine();
                    vals = line.Split('=');
                    fontsize = vals[1];
                    set.fntMain = new Font(fontname, float.Parse(fontsize));

                    // read font size
                }

                return set;
            } // wekamatrixfile exists
            else
                return null;
        } // LoadToFile


        /// <summary>
        /// saves the current settings object to a wekamatrixfile in the same folder as the executable
        /// </summary>
        public void SaveToFile()
        {
            string filename = ""; // Methods.getFileNamePath(System.Windows.Forms.Application.ExecutablePath) + "\\" + Const.STR_SETTINGS_FILE;
            using (StreamWriter sw = new StreamWriter(filename))
            {

                sw.WriteLine("BaseColor=" + colBase.R.ToString() + "," + colBase.G.ToString() + "," + colBase.B.ToString());
                sw.WriteLine("FontFamily=" + fntMain.FontFamily.Name);
                sw.WriteLine("FontSize=" + fntMain.Size.ToString());

            } // using writer

        } // SaveToFile



    } // class Settings
}
