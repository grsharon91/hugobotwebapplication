using System;
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

        public async Task SendToDiscretization(string cli, bool isDone)
        {
            await callCMD(cli);
            isDone = true;
        } 

        private Task callCMD(string cli)
        {
            string output = "";
            return Task.Run(() =>
           {
               using (Process process = new Process())
               {
                   process.StartInfo.FileName = "CMD.exe";
                    //NEED CHANGES IN ARGUMENTS//
                    process.StartInfo.Arguments = "/c cd C:/Users/admin/Desktop/kfir && activate hugobot &&" + cli;
                   process.StartInfo.UseShellExecute = false;
                   process.StartInfo.RedirectStandardOutput = true;
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

