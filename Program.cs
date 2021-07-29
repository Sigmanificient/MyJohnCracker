using System;
using System.Diagnostics;
using System.IO;
using System.Security.Cryptography;
using System.Text;  

namespace MyJohnCracker
{
    public class Program
    {
        private static void Main(string[] args)
        {
            Stopwatch watch = Stopwatch.StartNew();
            SHA256 sha256Hash = SHA256.Create();

            Console.WriteLine(File.ReadAllText(@"ressources/asciiart/asciiart.txt"));

            string targetHash = File.ReadAllText(args[0]);
            string[] dictionary = File.ReadAllLines(args[1]);

            int c = 0;
            int maxC = dictionary.Length - 1;
            string hash = "";

            while (hash != targetHash && c < maxC)
            {
                c++;
                hash = GetHash(sha256Hash, dictionary[c]);
            }
            
            watch.Stop();
            long elapsed = watch.ElapsedMilliseconds;

            if (hash == targetHash)
            {
                Console.WriteLine("[" + elapsed + "ms]" + targetHash + " --> " + dictionary[c]);
            }
            else
            {
                Console.WriteLine("[" + elapsed + "ms] No hash found");
            }
        }

        private static string GetHash(HashAlgorithm hashAlgorithm, string input)
        {

            // Convert the input string to a byte array and compute the hash.
            byte[] data = hashAlgorithm.ComputeHash(Encoding.UTF8.GetBytes(input));

            // Create a new Stringbuilder to collect the bytes
            // and create a string.
            var sBuilder = new StringBuilder();

            // Loop through each byte of the hashed data
            // and format each one as a hexadecimal string.
            for (int i = 0; i < data.Length; i++)
            {
                sBuilder.Append(data[i].ToString("x2"));
            }

            // Return the hexadecimal string.
            return sBuilder.ToString();
            
            
        }

        // Verify a hash against a string.
        private static bool VerifyHash(HashAlgorithm hashAlgorithm, string input, string hash)
        {
            // Hash the input.
            var hashOfInput = GetHash(hashAlgorithm, input);

            // Create a StringComparer an compare the hashes.
            StringComparer comparer = StringComparer.OrdinalIgnoreCase;

            return comparer.Compare(hashOfInput, hash) == 0;
        }
    }
}