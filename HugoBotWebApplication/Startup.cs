using Microsoft.Owin;
using Owin;

[assembly: OwinStartupAttribute(typeof(HugoBotWebApplication.Startup))]
namespace HugoBotWebApplication
{
    public partial class Startup
    {
        public void Configuration(IAppBuilder app)
        {
            ConfigureAuth(app);
        }
    }
}
