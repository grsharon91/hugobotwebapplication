using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System;
using System.Collections.Generic;
using System.Text;


namespace HugoBotMVC.Services
{
    public static class Methods
    {

        public static Random rnd;

        /// <summary>
        /// 
        /// </summary>
        /// <param name="from"></param>
        /// <param name="to"></param>
        /// <returns></returns>
        public static int getRandomNumber(int from, int to)
        {
            if (rnd == null)
                rnd = new Random();
            return rnd.Next(from, to);
        } // getRandomNumber


        public static int[] getRandomNumbers(int count, int from, int to, int[] exclude)
        {
            int i, num;
            List<int> ans = new List<int>();
            for (i = 0; i < count; i++)
            {
                num = getRandomNumber(from, to);
                while (Arrays.isMember(num, exclude) != -1 || ans.IndexOf(num) != -1)
                    num = getRandomNumber(from, to);
                ans.Add(num);
            } // for numbers;
            ans.Sort();
            return ans.ToArray();
        } // getRandomNumbers


        /// <summary>
        /// return (n 2)
        /// </summary>
        /// <param name="n"></param>
        /// <returns></returns>
        public static int N_2(int n)
        {
            return n * (n - 1) / 2;
        } // N_2


        /// <summary>
        /// Replaces all spaces with underlines
        /// </summary>
        /// <param name="str">string to convert</param>
        /// <returns>converted string</returns>
        public static string makeLegal(string str)
        {
            return str.Replace(' ', '_');
        }//Make Legal

        /// <summary>
        /// get wekamatrixfile's name given a full path string
        /// </summary>
        /// <param name="path">full path string</param>
        /// <returns>wekamatrixfile name without extension</returns>
        public static string getFileNameNoExt(string path)
        {
            return path.Substring(path.LastIndexOf('\\') + 1, path.LastIndexOf('.') - path.LastIndexOf('\\') - 1);
        } // getFileNameNoExt

        /// <summary>
        /// get wekamatrixfile's name given a full path string
        /// </summary>
        /// <param name="path">full path string</param>
        /// <returns>wekamatrixfile name including extension</returns>
        public static string getFileNameIncExt(string path)
        {
            return path.Substring(path.LastIndexOf('\\') + 1, path.Length - path.LastIndexOf('\\') - 1);
        } // getFileNameNoExt


        /// <summary>
        /// get wekamatrixfile's name given a full path string
        /// </summary>
        /// <param name="path">full path string</param>
        /// <returns>wekamatrixfile name without extension</returns>
        public static string getFileNameExtension(string path)
        {
            return path.Substring(path.LastIndexOf('.') + 1, path.Length - path.LastIndexOf('.') - 1);
        } // getFileNameNoExt



        /// <summary>
        /// get wekamatrixfile's path (no wekamatrixfile name) given a full path string
        /// </summary>
        /// <param name="path">full path string</param>
        /// <returns>path no wekamatrixfile</returns>
        public static string getFileNamePath(string path)
        {
            return path.Substring(0, path.LastIndexOf('\\'));
        }//getFileNamePath




        public class Arrays
        {

            public static string getArrayString(int[] arr)
            {

                string ans = "";
                for (int i = 0; i < arr.Length; i++)
                    ans += arr[i].ToString() + "-";
                return ans;

            } // getArrayString

            public static string getArrayString(long[] arr)
            {

                string ans = "";
                for (int i = 0; i < arr.Length; i++)
                    ans += arr[i].ToString() + "-";
                return ans;

            } // getArrayString


            /// <summary>
            /// given an integers array, will return the index of found item, -1 if not found
            /// </summary>
            /// <param name="toFind">item to find</param>
            /// <param name="arr">array to look in</param>
            /// <returns>item's index, -1 for no found</returns>
            public static int isMember(int toFind, int[] arr)
            {
                bool ans = false;
                int i = 0;
                while (!ans && i < arr.Length)
                    if (arr[i++] == toFind) ans = true;

                return ans ? i - 1 : -1;
            } // isMember

            /// <summary>
            /// given a longs array, will return the index of found item, -1 if not found
            /// </summary>
            /// <param name="toFind">item to find</param>
            /// <param name="arr">array to look in</param>
            /// <returns>item's index, -1 for no found</returns>
            public static int isMember(long toFind, long[] arr)
            {
                bool ans = false;
                int i = 0;
                while (!ans && i < arr.Length)
                    if (arr[i++] == toFind) ans = true;

                return ans ? i - 1 : -1;
            } // isMember


            /// <summary>
            /// given a strings array, a new array containing times replicates of the original will be returned
            /// </summary>
            /// <param name="arr">strings array to replicate</param>
            /// <param name="times">times to replicate</param>
            /// <returns>replications array</returns>
            public static string[] duplicateArray(string[] arr, int times)
            {
                int i, j;
                string[] ans = new string[times * arr.Length];
                for (i = 0; i < arr.Length; i++)
                {
                    for (j = 0; j < times; j++)
                    {
                        ans[i * times + j] = arr[i];
                    }
                }
                return ans;

            } // duplicateArray

            /// <summary>
            /// converts a given strings array to doubles array
            /// </summary>
            /// <param name="arr"></param>
            /// <param name="skip">number of cells at start to skip</param>
            /// <returns>new doubles array</returns>
            public static double[] getDoubleArray(string[] arr, int skip)
            {
                double[] ans = new double[arr.Length - skip];
                for (int i = skip; i < arr.Length; i++)
                    ans[i - skip] = double.Parse(arr[i]);
                return ans;
            } // getDoubleArray



        } // sub class Arrays


        public class Statistics
        {

            public static double getTIV(LegoObjects.LegoInstancesList instances)
            {

                int i;

                double ans = 0;

                int n = instances.Instances.Count;
                int k = instances.lstAvgIntervals.Count;

                if (n == 0 || k == 0) return -1;

                foreach (LegoObjects.LegoInstance instance in instances.Instances)
                {
                    i = 0;
                    foreach (TimeSeries.TimeInterval interval in instance.Intervals)
                    {
                        ans += Math.Pow(interval.length() - instances.lstAvgIntervals[i++].length(), 2);
                    } // for each interval

                } // for each instance

                ans = Math.Sqrt(ans) / (n * k);

                return ans;
            }


        }

    } // class Methods
}
