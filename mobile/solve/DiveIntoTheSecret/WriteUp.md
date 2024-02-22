# Dive Into The Secret
<p align="justify">
  As the statement says, to uncover the secret we need to get inside, and after the first challenge, we are in front of a login panel, so we can surmise that to obtain the second flag, we need to bypass the login panel. 
</p>

<table align="center" style="border-collapse: collapse; border: 4px solid #000;">
  <tr>
    <td style="padding: 5px; text-align: center;">
      <img src="./img/1.png">
    </td>
  </tr>
</table>

<p align="justify">
After analyzing the code, we observe that the application compares the provided username and password with a set of characters returned by various classes. If the provided credentials are correct, the MainActivity will call another activity named PostLogin. However, considering the tediousness of deobfuscating the code, which is not the primary intention of this challenge, we can use another powerful tool, drozer, to gain a general understanding of the application. 
</p>
<table align="center" style="border-collapse: collapse; border: 4px solid #000;">
  <tr>
    <td style="padding: 5px; text-align: center;">
      <img src="./img/2.png">
    </td>
  </tr>
</table>
We can run these two commands using drozer.
<div style="background-color: #f8f8f8; padding: 10px; overflow-y: auto; max-height: 300px; display: flex; justify-content: center; align-items: center;">
<pre style="font-size: 1.2em; margin: 0; padding-left: 0;">
<code style="font-size: 2em; display: inline-block; text-align: center;">run app.package.attacksurface com.android.hackon</code>
</pre>

<div style="background-color: #f8f8f8; padding: 10px; overflow-y: auto; max-height: 300px; display: flex; justify-content: center; align-items: center;">
<pre style="font-size: 1.2em; margin: 0; padding-left: 0;">
<code style="font-size: 2em; display: inline-block; text-align: center;">run app.activity.info -a com.android.hackon</code>
</pre>


<p align="justify">
We can see in the following image, the tool has discovered two exportable activities, one of them being PostLogin, which is the activity we observed in the previous code and quite suspicious. Since it is exportable, we can invoke this activity using adb. 
</p>

<table align="center" style="border-collapse: collapse; border: 4px solid #000;">
  <tr>
    <td style="padding: 5px; text-align: center;">
      <img src="./img/3.png">
    </td>
  </tr>
</table>

<p align="justify">
To trigger the activity, we can simply open adb shell in the terminal and enter the following command to invoke it.
</p>

<div style="background-color: #f8f8f8; padding: 10px; overflow-y: auto; max-height: 300px; display: flex; justify-content: center; align-items: center;">
<pre style="font-size: 1.2em; margin: 0; padding-left: 0;">
<code style="font-size: 2em; display: inline-block; text-align: center;">adb shell
am start –n com.android.hackon/.PostLogin</code>
</pre>
  
<table align="center" style="border-collapse: collapse; border: 4px solid #000;">
  <tr>
    <td style="padding: 5px; text-align: center;">
      <img src="./img/4.png">
    </td>
  </tr>
</table>


<p align="justify">
We can observe that after invoking the activity PostLogin, we are now inside, and on the home page, we have our flag. 
</p>
<table align="center" style="border-collapse: collapse; border: 4px solid #000;">
  <tr>
    <td style="padding: 5px; text-align: center;">
      <img src="./img/5.png">
    </td>
  </tr>
</table>

*Author: Lamp*
