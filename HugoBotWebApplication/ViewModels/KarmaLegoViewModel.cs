using System.ComponentModel.DataAnnotations;

namespace HugoBotWebApplication.ViewModels
{
    public class KarmaLegoViewModel
    {
        [Required]
        public int MinimumVerticalSupport { get; set; }
        [Required]
        public int MaximumGap { get; set; }
        [Required]
        public double Epsilon { get; set; }
        [Required]
        public string DatasetName { get; set; }
        [Required]
        public string Path { get; set; }
        [Required]
        public string VmapPath { get; set; }
        [Required]
        public string Category { get; set; }
        [Required]
        public string Visibility { get; set; }
    }
}