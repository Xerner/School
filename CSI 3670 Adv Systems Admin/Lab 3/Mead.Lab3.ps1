# Lab 3 – AD PowerShell Basics
# Name: Kenny Mead
# Date: 2021-02-10
# Description: Adds users read from a file Names.txt to the Administrators group

import-module ActiveDirectory

$users = import-csv Names.txt
foreach ($user in $users)
{
  # Required information
  #   - First Name
  #   - Last Name
  # Optional information
  #   - Street address
  #   - Mobile phone
  #   - Email address
  #   - Job title

  $ou = "CN=Users,DC=csi3670,DC=local"
  $pw = "Ch@ng3M31mm3d1@t3ly"
  $detailed_name = $user.FirstName + " " + $user.LastName
  $firstletter_first_name = $user.FirstName.Substring(0,1)
  $SAM = $firstletter_first_name + $user.LastName


  # This must all be on a single line
  New-AdUser -Name $SAM -SamAccountName $SAM -UserPrincipalName $SAM -DisplayName $detailed_name `
            -GivenName $user.FirstName -Surname $user.LastName -AccountPassword (ConvertTo-SecureString $pw -AsPlainText -Force) `
            -StreetAddress $user.Address -MobilePhone $user.PhoneNumber -EmailAddress $user.EmailAddress -Title $user.JobTitle `
            -Enabled $true -Path $ou -PassThru | % {Add-ADGroupMember -Identity "Administrators" -Members $_}
}
