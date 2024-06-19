if (Get-Command -Name "python" -ErrorAction SilentlyContinue)
{
	Write-Host "Python is already installed!"
}
else
{
	Write-Host "Install python and execute the script again!"
	Start-Process ms-windows-store://pdp?productid=9nrwmjp3717k
	exit 1
}

Write-Host "Creating virtual environment..."
python3 -m venv venv

Write-Host "Activating virtual environment"
.\\venv\\Scripts\\activate

Write-Host "Installing requirements..."
pip install -r requirements.txt

Write-Host "Done! Now you can run: py AutoEndorse.py"
Write-Host "When you are finished, run: deactivate"
