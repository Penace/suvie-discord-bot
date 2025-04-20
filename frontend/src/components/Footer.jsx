export default function Footer() {
  return (
    <footer className="w-full max-w-5xl mt-20 text-center text-sm text-zinc-500 dark:text-zinc-400">
      © 2025 suvie by{" "}
      <a
        href="https://penace.org"
        className="underline"
        target="_blank"
        rel="noopener noreferrer"
      >
        Penace
      </a>{" "}
      •{" "}
      <a
        href="https://github.com/Penace/"
        className="underline"
        target="_blank"
        rel="noopener noreferrer"
      >
        GitHub
      </a>{" "}
      •{" "}
      <a href="/#/docs" className="underline">
        Docs
      </a>{" "}
      •{" "}
      <a href="/#/support" className="underline">
        Support
      </a>{" "}
      •{" "}
      <a href="/#/roadmap" className="underline">
        Roadmap
      </a>{" "}
      •{" "}
      <a
        href="https://ko-fi.com/penace"
        className="underline text-pink-500"
        target="_blank"
        rel="noopener noreferrer"
      >
        Ko-fi
      </a>{" "}
      •{" "}
      <a
        href="https://www.buymeacoffee.com/penace"
        className="underline text-yellow-600"
        target="_blank"
        rel="noopener noreferrer"
      >
        Buy Me a Coffee
      </a>
    </footer>
  );
}
