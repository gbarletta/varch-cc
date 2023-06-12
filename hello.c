int fibonacci(int n)
{
  int ciao;
  ciao = 40;
  if (n <= 1)
    return n;
  else
    return fibonacci(n - 1) + fibonacci(n - 2);
}

int main()
{
  int i = 8;
  return fibonacci(10);
}