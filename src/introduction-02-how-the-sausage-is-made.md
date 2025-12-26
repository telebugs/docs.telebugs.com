# How the sausage is made

Telebugs uses proven and reliable technologies. Knowing the stack matters. When
you buy Telebugs, you get the full source code. You own it for life. You can
modify it any way you like (just don't share it, since Telebugs is not open
source. See the [Software License Agreement][2]).

Telebugs builds on these technologies:

- **Ruby on Rails:** A Ruby web framework with decades behind it. Simple and
  boring. No revolution needed here.

- **Turbo:** This covers the set of tools that power modern Rails apps out of
  the box. Thanks to Turbo (and the next item), Telebugs skips JavaScript
  frameworks entirely. Proven, simple, and easy to maintain.

- **Stimulus:** Think of it as jQuery for 2025, but even simpler, since
  JavaScript has improved a lot.

- **Solid Queue:** Handles background jobs, like sending error notifications.
  This lets Telebugs run without Redis. Fewer dependencies to deal with.

- **SQLite:** The real MVP of the stack. A fantastic library that needs no
  introduction and almost zero administration.

That’s it! Error processing really can be this simple.

So is Telebugs only for Rails devs? _No._ You never have to touch the code if you
don’t want to. You can read it, sure. It’s pure Ruby. Probably the most readable
programming syntax out there. It almost feels like English.

Not familiar with [Ruby][1]? Pair it with your favorite LLM and tweak away. That
said, I don’t expect you to need that. Telebugs ships with everything essential.

Telebugs isn’t here to change the world. It’s here to leave you alone. And
that’s exactly the point.

[1]: https://www.ruby-lang.org/en/
[2]: /appendix-01-software-license-agreement.md
