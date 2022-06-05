using Newtonsoft.Json;
public class Datum
{
    public string? age { get; set; }
    public string? workclass { get; set; }
    public double? fnlwgt { get; set; }
    public string? education { get; set; }

    [JsonProperty("education-num")]
    public double? EducationNum { get; set; }

    [JsonProperty("marital-status")]
    public string? MaritalStatus { get; set; }
    public string? occupation { get; set; }
    public string? relationship { get; set; }
    public string? race { get; set; }
    public string? sex { get; set; }
    public string? capitalgain { get; set; }
    public string? capitalloss { get; set; }
    public string? hoursperweek { get; set; }
    public string? predicted { get; set; }
}

public class Root
{
    public List<Datum>? data { get; set; }
}
