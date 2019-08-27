namespace HugoBotWebApplication.Migrations
{
    using System;
    using System.Data.Entity.Migrations;
    
    public partial class mymigration : DbMigration
    {
        public override void Up()
        {
            DropColumn("dbo.Datasets", "Path");
            DropColumn("dbo.Datasets", "VmapPath");
        }
        
        public override void Down()
        {
            AddColumn("dbo.Datasets", "VmapPath", c => c.String(nullable: false));
            AddColumn("dbo.Datasets", "Path", c => c.String(nullable: false));
        }
    }
}
