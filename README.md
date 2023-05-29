# pabaraianalytics

# Visualize Your Data with Ease
Effortless Data Visualization: Seamlessly Generate Line, Bar, Histogram, and Plotly Charts from CSV Uploads

This is a Streamlit application that allows you to visualize your data using various types of charts. You can upload a CSV file and select the type of chart you want to generate.

## Prerequisites

Before running the application, make sure you have the following dependencies installed:

- Streamlit
- Matplotlib
- Pandas
- Plotly Express
- Pillow
- Firebase Admin SDK
- re (regular expression module)

You can install the dependencies by running the following command:

```bash
pip install streamlit matplotlib pandas plotly Pillow firebase-admin
 
## Firebase Setup
To use the Firebase authentication and database functionality, you need to set up a Firebase project and obtain the service account credentials. Follow the steps below to set up Firebase:

Go to the Firebase Console and create a new project.
In the project settings, navigate to the "Service Accounts" tab.
Click on the "Generate new private key" button to download the service account credentials file in JSON format.
Save the downloaded JSON file to the same directory as the application code and rename it to pabaranalytics-firebase-adminsdk-th0qb-1efdb39cf3.json (or update the cred = credentials.Certificate('pabaranalytics-firebase-adminsdk-th0qb-1efdb39cf3.json') line in the code with the correct file path).
Running the Application
To run the application, execute the following command:

bash
Copy code
streamlit run your_script.py
Replace your_script.py with the filename of the script containing the code provided above.

## Usage
Once the application is running, you will see the main page with the title "Visualize Your Data with Ease" and a description of the application.

## Menu
The sidebar on the left side of the page contains the following options:

- Login: Allows existing users to log in to the application.
- Daftar: Allows new users to sign up for an account.

## Login
If you click on the "Login" option in the sidebar, you will be taken to the login page. Enter your email and password and click the "Login" button to log in to the application. If the login is successful, you will see a success message, and the main menu will be displayed.

## Daftar
If you click on the "Daftar" option in the sidebar, you will be taken to the signup page. Enter your email, password, and confirm the password, then click the "Daftar" button to create a new account. If the signup is successful, you will see a success message, and you can proceed to log in.

## Menu Utama
After logging in, you will see the main menu with two options:

## Profil: Displays the user's email and provides a logout button.
Grafik: Allows you to select and generate different types of charts.
Profil
In the "Profil" section, you can view the email address associated with your account. Click the "Logout" button to log out of the application.

## Grafik
In the "Grafik" section, you can select the type of chart you want to generate. The available chart types are:

Line Chart: Displays a line chart based on data from a CSV file.
Bar Chart: Displays a bar chart based on data from a CSV file.
Histogram: Displays a histogram based on data from a CSV file.
Plotly Chart: Displays a scatter plot

## Author

This project is authored by Noer Barrihadianto. You can find more about the author on the following platforms:

- LinkedIn: [Noer Barrihadianto](https://www.linkedin.com/in/noerbarry/)
- GitHub: [noerbarri](https://github.com/noerbarry)

## Donation
If you find this project helpful and would like to support its development, you can contribute by buying me a coffee. Your support and contribution will be greatly appreciated.
<br>
<a href="https://www.buymeacoffee.com/noerbarry" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

By donating, you will help me continue working on this project, improving its features, and maintaining its functionality. Your contribution will directly contribute to the sustainability and growth of this project.

Thank you for your support!

Please note that donations are voluntary and non-refundable.


## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvement, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
