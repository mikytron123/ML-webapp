using System.ComponentModel.DataAnnotations;
using Newtonsoft.Json;
public class Model
{
    [Required]
    public string? age {get;set;}
    [JsonIgnore]
    public List<string> ages = new List<string>() {
        "0",
        "1",
        "2",
        "3"
    };

    [Required]
    public string? workclass {get;set;}
    [JsonIgnore]
    public List<string> workcat = new List<string>(){
        "State-gov",
        "Self-emp-not-inc",
        "Private",
        "Federal-gov",
        "Local-gov",
        "Self-emp-inc",
        "Without-pay"
    };

    [Required]
    [Range(13492,1490400)]
    public Single? fnlwgt {get;set;}

    [Required]
    public string? education {get;set;}
    [JsonIgnore]
    public List<string> educationcat = new List<string>(){
        "Bachelors",
        "HS-grad",
        "11th",
        "Masters",
        "9th",
        "Some-college",
        "Assoc-acdm",
        "Assoc-voc",
        "7th-8th",
        "Doctorate",
        "Prof-school",
        "5th-6th",
        "10th",
        "Preschool",
        "12th",
        "1st-4th"
        };
    [Required]
    public string? marital_status {get;set;}
    [JsonIgnore]
    public List<string> status = new List<string>(){
        "Never-married",
        "Married-civ-spouse",
        "Divorced",
        "Married-spouse-absent",
        "Separated",
        "Married-AF-spouse",
        "Widowed"
        };
    [Required]
    public string? occupation {get;set;}
    [JsonIgnore]
    public List<string> occ = new List<string>(){
        "Adm-clerical",
        "Exec-managerial",
        "Handlers-cleaners",
        "Prof-specialty",
        "Other-service",
        "Sales",
        "Craft-repair",
        "Transport-moving",
        "Farming-fishing",
        "Machine-op-inspct",
        "Tech-support",
        "Protective-serv",
        "Armed-Forces",
        "Priv-house-serv"
    };
    [Required]
    public string? relationship {get;set;}
    [JsonIgnore]
    public List<string> relation = new List<string>(){
        "Not-in-family",
        "Husband",
        "Wife",
        "Own-child",
        "Unmarried",
        "Other-relative"
    };

    [Required]
    public string? race {get;set;}
    [JsonIgnore]
    public List<string> racecat = new List<string>(){
        "White",
        "Black",
        "Asian-Pac-Islander",
        "Amer-Indian-Eskimo",
        "Other"
    };

    [Required]
    public string? sex {get;set;}
    [JsonIgnore]
    public List<string> sexcat = new List<string>(){
       "Male",
       "Female"
    };
    [Required]
    public string? capitalgain {get;set;}
    [JsonIgnore]
    public List<string> capitalgaincat = new List<string>(){
       "0",
       "1",
       "2",
       "3",
    };

    [Required]
    public string? capitalloss {get;set;}
    [Required]
    public string? hoursperweek {get;set;}

}