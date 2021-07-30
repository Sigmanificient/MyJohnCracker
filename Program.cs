using System;
using System.Diagnostics;
using System.IO;
using System.Security.Cryptography;
using System.Text;

namespace MyJohnCracker
{
    public static class Program
    {
        private static void Main(string[] args)
        {
            if (args.Length < 2)
            {
                Console.WriteLine(":argument:");
                Console.WriteLine("\t--help\t\tShow this helpful message\n");
                Console.WriteLine("\t:param[1]:\t\tHash path,\tdefault: [assets/hash]");
                Console.WriteLine("\t:param[2]:\t\tDictionary path,\tdefault: [assets/dict]");
                return;
            }

            var watch = Stopwatch.StartNew();
            var sha256Hash = SHA256.Create();

            Console.WriteLine(File.ReadAllText(@"resources/asciiart/asciiart.txt"));

            var targetHash = File.ReadAllText(args[0]);
            var dictionary = File.ReadAllLines(args[1]);

            var c = 0;
            var maxC = dictionary.Length - 1;
            var hash = "";

            while (hash != targetHash && c < maxC)
            {
                c++;
                hash = GetHash(sha256Hash, dictionary[c]);
            }

            watch.Stop();

            Console.Write($"[{watch.ElapsedMilliseconds.ToString()}ms] ");
            Console.WriteLine((hash == targetHash) ? $"{targetHash} --> {dictionary[c]}" : "No hash found");
        }

        private static string GetHash(HashAlgorithm hashAlgorithm, string input)
        {
            // Convert the input string to a byte array and compute the hash.
            var data = hashAlgorithm.ComputeHash(Encoding.UTF8.GetBytes(input));

            // Create a new String builder to collect the bytes
            // and create a string.
            // ReSharper disable once HeapView.ObjectAllocation.Evident
            var sBuilder = new StringBuilder();

            // Loop through each byte of the hashed data
            // and format each one as a hexadecimal string.
            foreach (var t in data) {
                sBuilder.Append(t.ToString("x2"))
            };

            // Return the hexadecimal string.
            return sBuilder.ToString();
        }
    }
}