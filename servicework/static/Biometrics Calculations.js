
/*
I couldnt figure out how to create a reference to this file from my flask environment so I put the javascript directly in my layout.html file. 
/*
####---BIOMETRICS CALCULATOR FUCTIONS---###
*/

function getVariables(){
    // Get all variables from HTML file. 
    var userName = document.getElementById("userName").value;
    var userWeightBiometric = document.getElementById("userWeightBiometric").value;
    var userHeight = document.getElementById("userHeight").value;
    var userAge = document.getElementById("userAge").value;
    var genderPick = document.getElementById('genderPick'); // Dropdown Item
    var genderPick = genderPick.options[genderPick.selectedIndex].text;
    var goalPick = document.getElementById("goalPick"); // Dropdown Item
    var goalPick = goalPick.options[goalPick.selectedIndex].text;
    // Test - Uncomment below to make sure all variables are accounted for. 
    //window.alert(`You entered stuff! ${userName}, ${userWeightBiometric}, ${userHeight}, ${userAge}, ${genderPick}, ${goalPick}`);
    
    // Test to make sure every field has been filled. If not, create alert window. 
    if(isNaN(userWeightBiometric) || isNaN(userHeight) || isNaN(userAge) || userName == "" || genderPick == "Choose one" || goalPick == "Select a goal"){
        window.alert("Please doublecheck that all of the fields have been filled in the biometrics table. Then, click 'submit'.")
        return
    }
    // Otherwise, proceed to next function to calculate the amount of calories the user needs per day [Basal Metabiolic Rate (BMR)].
    calculateBMR(userName, userWeightBiometric, userHeight, userAge, genderPick, goalPick)
}

function calculateBMR(  userName, userWeightBiometric, userHeight, userAge, genderPick, goalPick){
    // This function establishes a daily calorie expenditure based on user biometrics.
    // https://www.thecalculatorsite.com/health/bmr-calculator.php
    if(genderPick=="Male"){
        // Perform male Mifflin - St Jeor formula for men
        var userBMR = (4.536 * userWeightBiometric) + (15.88 * userHeight) - (5 * userAge) + 5;
    }
    else if(genderPick=="Female"){
        // Perform female Mifflin - St Jeor formula for women
        var userBMR = (4.536 * userWeightBiometric) + (15.88 * userHeight) - (5 * userAge) - 161;
    }
    // We are defaulting to "sedentary lifestyle" multiplier for simplicity. If people were active, the multiplier would go up and they would burn more calories. 
    newBMR = Math.ceil(userBMR * 1.2);
    // Test - Uncomment below to make sure the TDEE variable is working.
    // window.alert(`Your TDEE has been calculated and is ${newBMR}`)
    
    // Proceed to function to create new variables if the user wants to lose, maintain, or gain weight.
    calculateResults(newBMR, userName, goalPick)
}

function calculateResults(newBMR, userName, goalPick){
    // This function handles whether the user wants to lose, maintain, or gain weight. It modifies calorie total based on user goal.
    if(goalPick == "Lose Weight") {
        var modifiedBMR = (newBMR - (newBMR * 0.15));
    }
    else if(goalPick == "Maintain Weight"){
        var modifiedBMR = (newBMR); 
    }
    else if(goalPick == "Gain Weight"){
        var modifiedBMR = (newBMR + (newBMR * 0.15));
    }
    // This calculates actual grams of type of food based on calorie total
    var dailyProtein = (modifiedBMR * 0.42) / 4;
    var dailyCarbs = (modifiedBMR * 0.38) / 4;
    var dailyFat = (modifiedBMR * 0.20) / 9;
    
    // Proceed to function that prints the results. 
    displayResults(goalPick, newBMR, modifiedBMR, dailyProtein, dailyCarbs, dailyFat, userName)
}

function displayResults(goalPick, newBMR, modifiedBMR, dailyProtein, dailyCarbs, dailyFat, userName){
    // This is the final function called from the above process for the feedback window.
    var results = document.getElementById("resultsTextArea").value =
        `${userName}'s results: \n\no TDEE (Total Daily Energy Expenditure): ${newBMR} Calories\no Recommended Daily Calorie Intake: ${modifiedBMR} 
        \nIn order to ${goalPick}, that's how many calories you need to eat per day.\n\nYour daily recommended Macro-Nutrients are:
        \no Carbs: ${Math.ceil(dailyCarbs)} grams\no Protein: ${Math.ceil(dailyProtein)} grams\no Fats: ${Math.ceil(dailyFat)} grams
        \nIf eating 3 equal meals a day, one meal should resemble the following:
        \no Carbs: ${Math.ceil(dailyCarbs* 0.33)} grams\no Protein: ${Math.ceil(dailyProtein * 0.33)} grams \no Fats: ${Math.ceil(dailyFat * 0.33)} grams`
}
