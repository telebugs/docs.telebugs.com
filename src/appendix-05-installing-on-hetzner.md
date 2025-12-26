# Installing on Hetzner

Hosting Writebook on [Hetzner](https://www.hetzner.com/) is a smart pick. It’s
budget-friendly and simple to set up if you’re comfortable with some basic tech
steps.

**After signing up for a Hetzner account**, follow these steps. It should take
about 5 minutes.

1. In your Hetzner account, click **+ Create Server** and pick a plan.

   ![Creating a new Hetzner server](assets/images/appendix-05-installing-on-hetzner/01.webp)

   You need at least 2GB RAM and 1 CPU.

   ![CPU type selection](assets/images/appendix-05-installing-on-hetzner/02.webp)

2. Keep the default settings and click **Create and Buy now**. Your server will
   be ready in a few minutes.

3. Once it’s ready, copy the **Public IP** address. This links your domain to
   the server.

   ![Public IP of a server](assets/images/appendix-05-installing-on-hetzner/03.webp)

4. Go to your domain provider’s site (like [GoDaddy](https://www.godaddy.com/),
   [namecheap](https://www.namecheap.com/), or
   [Cloudflare](https://www.cloudflare.com/)). Log in, find the domain
   management section, and add an `A record` with the IP you copied. It should
   look like this:

   ![A record configuration](assets/images/appendix-05-installing-on-hetzner/04.webp)

   Ensure that proxying is disabled.

5. Back in Hetzner, open the Console to connect to your server.

   ![The Console option](assets/images/appendix-05-installing-on-hetzner/05.webp)

6. Check the confirmation email we sent you for the install command. Paste it
   into the command line.

   ![Telebugs installation script](assets/images/appendix-05-installing-on-hetzner/06.webp)

7. When prompted, type your domain name (the same one you used for the A
   record). The system will finish the setup. After a few minutes, you’ll see
   this:

   ![Telebugs installation complete](assets/images/appendix-05-installing-on-hetzner/07.webp)

8. All set! Open the URL in your browser and create your Telebugs account.
