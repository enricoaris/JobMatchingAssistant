using UglyToad.PdfPig;
using UglyToad.PdfPig.Content;
using UglyToad.PdfPig.DocumentLayoutAnalysis.TextExtractor;

namespace MatchEngine.Api.Helper
{
    public class PdfHelper
    {
        public string Extract(string filepath)
        {
            var resultText = "";

            using (PdfDocument document = PdfDocument.Open(filepath))
            {
                foreach (Page page in document.GetPages())
                {
                    string text = ContentOrderTextExtractor.GetText(page);
                    resultText += text + "\n";
                }
            }

            return resultText;
        }
    }
}
