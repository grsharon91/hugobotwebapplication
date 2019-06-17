using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Data.Entity;
using System.Linq;
using System.Web;

namespace HugoBotWebApplication.Models
{
    public class ViewPermissions
    {
        [Key]
        public string Key { get; set; }
        public string UserName { get; set; }
        public int DatasetID { get; set; }
    }

}