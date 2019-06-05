using HugoBotWebApplication.Models;
using Microsoft.AspNet.Identity;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace HugoBotWebApplication.Services
{
    public class EmailService
    {
        public bool SendConfirmationEmail(ApplicationUser user, string callbackUrl)
        {
           
            System.Net.Mail.MailMessage m = new System.Net.Mail.MailMessage(
            new System.Net.Mail.MailAddress("donotreply@hugobot.bgu.ac.il", "Hugobot email confirmation"),
            new System.Net.Mail.MailAddress(user.Email))
            {
                Subject = "Email confirmation",
                Body = 

                "Dear " + user.FirstName + " " + user.LastName + "," +    
                "<BR/> " +
                "Thank you for your registration, " +
                "After clicking the link below, an email will be sent to the hugobot support in order to  " +
                "confirm your identity, please be patient. " +
                "<a href=\"" + callbackUrl + "\">link</a><br/>" ,
            
                IsBodyHtml = true
            };
            System.Net.Mail.SmtpClient smtp = new System.Net.Mail.SmtpClient("smtp.gmail.com", 587)
            {
                Credentials = new System.Net.NetworkCredential("hugobotsupp@gmail.com", "hugoHugoBot8102"),
                //smtp.Sem = () => true; //Solution for client certificate error
                EnableSsl = true
            };
            smtp.Send(m);
            return true;
        }
        public bool SendAdminConfirmationEmail(ApplicationUser user, string authorizeCallbackUrl, string rejectCallbackUrl)
        {

            System.Net.Mail.MailMessage m = new System.Net.Mail.MailMessage();
            m.From = new System.Net.Mail.MailAddress("hugobotsupp@gmail.com", "Hugobot new account confirmation");
            m.To.Add("hugobotsupp@gmail.com");
            m.To.Add("robertmo@bgu.ac.il");

            m.Subject = "Hugobot new account confirmation";
            m.Body = "A new account wants to register: <br>" +
                "Email: " + user.Email + "<br>" + "Name: " + user.FirstName + " " + user.LastName + "<br>"  + "Institute: " + user.Institute + "<br>" +
                "Confirm the account by clicking this link: <a href=\"" + authorizeCallbackUrl + "\">link</a><br/>" +
                "<br> Or reject the account by clicking this link :  <a href=\"" + rejectCallbackUrl + "\">link</a><br/>";
            
            m.IsBodyHtml = true;
            System.Net.Mail.SmtpClient smtp = new System.Net.Mail.SmtpClient("smtp.gmail.com", 587)
            {
                Credentials = new System.Net.NetworkCredential("hugobotsupp@gmail.com", "hugoHugoBot8102"),
                //smtp.Sem = () => true; //Solution for client certificate error
                EnableSsl = true
            };
            smtp.Send(m);

            return true;
        }
        public bool SendForgotPasswordEmail(ApplicationUser user, string callbackUrl)
        {
            System.Net.Mail.MailMessage m = new System.Net.Mail.MailMessage(
            new System.Net.Mail.MailAddress("donotreply@hugobot.bgu.ac.il", "Hugobot Support Team"),
            new System.Net.Mail.MailAddress(user.Email))
            {
                Subject = "Hugobot password reset",
                Body =
                "Hey there, <br />" +
                "<br />" +
                "We've just recieved a request to reset the password to your account, you can complete the password reset process by following this link: <a href=\"" + callbackUrl + "\">here</a><br/>" +
                "If you believe you've recieved this email by accident, please ignore this email.<br />" +
                "<br />" +
                "Hugobot Support Team",
                IsBodyHtml = true
            };
            System.Net.Mail.SmtpClient smtp = new System.Net.Mail.SmtpClient("smtp.gmail.com", 587);
            smtp.Credentials = new System.Net.NetworkCredential("hugobotsupp@gmail.com", "hugoHugoBot8102");
            //smtp.Sem = () => true; //Solution for client certificate error
            smtp.EnableSsl = true;
            smtp.Send(m);
            return true;
        }
        
    }
}