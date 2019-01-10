using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Web;

namespace HugoBotWebApplication.Utils.FileHandlers
{
    interface IFileHandler<T>
    {
        T[] ReadFileToArray(string path);
        byte[] GetBytesFromFile(string path);
        byte[] GetBytesFromArray(T[] fileArray);
        void WriteFile(string path);
        object ValidateFileBase(HttpPostedFileBase fileBase);
        T[] ReadHttpPostedFileBaseToArray(HttpPostedFileBase fileBase);

    }
}
