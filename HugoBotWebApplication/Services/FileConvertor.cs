using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.IO;
using System.Web.Mvc;
using System.Runtime.Serialization.Formatters.Binary;
using System.Text;

namespace HugoBotMVC.Services
{
    public class FileConvertor
    {
        public static List<object> parseByteArrToIndex(byte[] byteArr)
        {
            string line;
            List<object> result = new List<object>();

            using (StreamReader sr = new StreamReader(new MemoryStream(byteArr), Encoding.Default))
            {
                while ((line = sr.ReadLine()) != null)
                {
                    string[] parts = line.Split(' ');
                    string path = sr.ReadLine();
                    result.Add(
                        new
                        {
                            StateID = parts[1].Split('-')[0], // remove the '-' in  the name of chunck
                            relation = parts[2],
                            orizontalSupport = parts[3],
                            vertical = parts[4],
                            path
                        }
                    );
                }
            }
            return result;
        }
    }
}