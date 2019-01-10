using System;
using System.Collections.Generic;
using System.Text;
using System.IO;

namespace HugoBotMVC
{
    public class KarmaFileReader : IDisposable 
    {
        StreamReader sr;

        public KarmaFileReader(byte[] byteArr)
        {
            sr = new StreamReader(new MemoryStream(byteArr), Encoding.Default);
        }


        public KarmaFileReader(string filename)
        {
            sr = new StreamReader(filename);
        }

        ~KarmaFileReader()
        {
            sr.Close();
        }

        public string getWord()
        {
            char[] buff = new char[1];
            StringBuilder str = new StringBuilder(100);
            if (!sr.EndOfStream)
                sr.Read(buff, 0, 1);
            else
                return null;
            while (buff[0] != ' ' && buff[0] != (char)13 && buff[0] != (char)10)
            {
                str.Append(buff[0]);
                if (!sr.EndOfStream)
                    sr.Read(buff, 0, 1);
                else
                    return str.ToString();
            }
            return str.ToString().Trim();

        } // 


        /// <summary>
        /// read a whole line and return it as a string. notice this shouldn't be used on an instances line!!!  
        /// </summary>
        /// <returns>read line</returns>
        public string getLine()
        {
            string word, line = "";
            while ((word = getWord()) != null && word != "" && word != ";") line += word + " ";
            /*
             * if (!sr.EndOfStream)
                sr.ReadLine();
            else
                return null;*/
            if (line.Length > 0) return line.Trim();
            if (word == null || sr.EndOfStream) return null;
            return line.Trim();

        } // getLine


        /// <summary>
        /// skips current line in the file.
        /// </summary>
        public void skipLine()
        {
            string word;
            //kr.ReadLine();
            while ((word = getWord()) != ";");
            sr.ReadLine();
        } // skipLine


        /// <summary>
        /// skip a line by reading it fully in the file. Do not use on instances line!!!
        /// </summary>
        public void readLine()
        {
            sr.ReadLine();
        }

        /// <summary>
        /// IDisposable interface - Dispose
        /// </summary>
        public void Dispose()
        {
            sr.Close();
        }


        public void copyLine(StreamWriter destwriter)
        {

            string word;
            //kr.ReadLine();
            while ((word = getWord()) != ";")
            {
                if (word != "")
                    destwriter.Write(word + " ");
            }
            destwriter.WriteLine(word); // write ;
            readLine();
           
        } // copyLine
    }
}
