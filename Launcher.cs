using System;
using System.Diagnostics;
using System.IO;

namespace RAM_Launcher
{
    class Program
    {
        static void Main(string[] args)
        {
            string path = Path.Combine(Environment.CurrentDirectory, "Roblox Manager.exe");

            if (File.Exists(path))
                Process.Start(path);

            Environment.Exit(0);
        }
    }
}
