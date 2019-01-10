using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;

// see http://stackoverflow.com/questions/3975741/column-headers-in-csv-using-filehelpers-library/8258420#8258420

// ReSharper disable CheckNamespace
namespace FileHelpers
// ReSharper restore CheckNamespace
{
    [AttributeUsage(AttributeTargets.Field, AllowMultiple = false, Inherited = true)]
    public class FieldTitleAttribute : Attribute
    {
        public FieldTitleAttribute(string name)
        {
            if (name == null) throw new ArgumentNullException("name");
            Name = name;
        }

        public string Name { get; private set; }
    }

    public static class FileHelpersTypeExtensions
    {
        public static IEnumerable<string> GetFieldTitles(this Type type)
        {
            var fields = from field in type.GetFields(
                BindingFlags.GetField |
                BindingFlags.Public |
                BindingFlags.NonPublic |
                BindingFlags.Instance)
                         where field.IsFileHelpersField()
                         select field;

            return from field in fields
                   let attrs = field.GetCustomAttributes(true)
                   let order = attrs.OfType<FieldOrderAttribute>().Single().GetOrder()
                   let title = attrs.OfType<FieldTitleAttribute>().Single().Name
                   orderby order
                   select title;
        }

        public static string GetCsvHeader(this Type type)
        {
            return String.Join(",", type.GetFieldTitles());
        }

        static bool IsFileHelpersField(this FieldInfo field)
        {
            return field.GetCustomAttributes(true)
                .OfType<FieldOrderAttribute>()
                .Any();
        }

        static int GetOrder(this FieldOrderAttribute attribute)
        {
            // Hack cos FieldOrderAttribute.Order is internal (why?)
            var pi = typeof(FieldOrderAttribute)
                .GetProperty("Order",
                    BindingFlags.GetProperty |
                    BindingFlags.Instance |
                    BindingFlags.NonPublic);

            return (int)pi.GetValue(attribute, null);
        }
    }
}