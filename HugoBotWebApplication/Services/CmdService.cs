﻿using System;
using System.IO;
using System.Diagnostics;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Threading.Tasks;

namespace HugoBotWebApplication.Services
{
    public class CmdService
    {

        public async Task SendToCMD(string cli, string fileToProccess)
        {
            await callCMD(cli, fileToProccess);

        }

        private Task callCMD(string cli, string fileToProccess)
        {
            string output = "";
            return Task.Run(() =>
            {
                using (Process process = new Process())
                {
                    process.StartInfo.FileName = "CMD.exe";
                    string path = "App_Data/" + fileToProccess;
                    string fullPath = Path.Combine(HttpRuntime.AppDomainAppPath, path);
                    process.StartInfo.Arguments = "/c cd " + fullPath + " && " + cli;
                    process.StartInfo.UseShellExecute = false;
                    process.StartInfo.RedirectStandardInput = true;
                    process.StartInfo.RedirectStandardOutput = true;
                    process.StartInfo.RedirectStandardError = true;
                    process.Start();

                    // Synchronously read the standard output of the spawned process. 
                    StreamReader reader = process.StandardOutput;
                    output = reader.ReadToEnd();

                    // Write the redirected output to this application's window.
                    Console.WriteLine(output);

                    process.WaitForExit();
                }
            });

            // Console.WriteLine("\n\nPress any key to exit.");
            //  Console.ReadLine();
            //    return output;                          
        }
    }
}