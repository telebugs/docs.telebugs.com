# Installing on DigitalOcean

Using [Digital Ocean](https://www.digitalocean.com) to host Telebugs is a great
choice. It’s affordable and easy to set up.

**After signing up for a Digital Ocean account**, follow these steps. It should
take about 5 minutes.

1. In your Digital Ocean account, go to `Create > Droplets` and pick a plan for
   your server.

   ![Creating a new Digital Ocean droplet](assets/images/appendix-04-installing-on-digital-ocean/01.webp)

   You need at least 2GB RAM and 1 CPU.

   ![Regular CPU with a regular SSD](assets/images/appendix-04-installing-on-digital-ocean/02.webp)

2. Set a password to connect to your server.

   ![Choosing authentication method](assets/images/appendix-04-installing-on-digital-ocean/03.webp)

3. Leave the other settings as they are and click **Create Droplet**. Wait a few
   minutes for it to be ready, then click it.

   ![List of droplets for the Telebugs project](assets/images/appendix-04-installing-on-digital-ocean/04.webp)

4. Copy the `ipv4` address. You’ll use it to link your domain to this server.

   ![IP v4 address copying](assets/images/appendix-04-installing-on-digital-ocean/05.webp)

   Go to your domain provider’s site (like [GoDaddy](https://www.godaddy.com/),
   [namecheap](https://www.namecheap.com/), or
   [Cloudflare](https://www.cloudflare.com/)). Log in, find the domain
   management section, and add an `A record` with the IP you copied. It should
   look like this:

   ![A record configuration](assets/images/appendix-04-installing-on-digital-ocean/06.webp)

   Ensure that proxying is disabled.

5. Back in Digital Ocean, find your Droplet and open the **Console** to access
   your server.

   ![Droplet console link](assets/images/appendix-04-installing-on-digital-ocean/07.webp)

6. Check the confirmation email we sent you for the install command. Paste it
   into the command line.

   ![Telebugs installation script](assets/images/appendix-04-installing-on-digital-ocean/08.webp)

7. When prompted, type your domain name (the same one you used for the A
   record). The system will finish the setup. After a few minutes, you’ll see
   this:

   ![Telebugs installation complete](assets/images/appendix-04-installing-on-digital-ocean/09.webp)

8. All set! Open the URL in your browser and create your Telebugs account.
