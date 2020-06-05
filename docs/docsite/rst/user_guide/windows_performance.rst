.. _windows_performance:

Windows パフォーマンス
===================
本書では、特に Ansible をそのホストで使用するような状況、
および一般的に使用する状況で高速化するために、
Windows ホストに適用するパフォーマンスの最適化をいくつか説明します。

Ansible タスクのオーバーヘッドを軽減するための PowerShell のパフォーマンスの最適化
---------------------------------------------------------------
PowerShell の起動を約 10 倍高速化するには、
Administrator セッションで以下の PowerShell スニペットを実行します。数十秒かかることが
予想されます。

.. note::

    ngen タスクまたはサービスでネイティブイメージがすでに作成されている場合は、
    パフォーマンスに違いは見られません (ただし、この時点では、
    他の場合よりも高速に実行されます)。

.. code-block:: powershell

    function Optimize-PowershellAssemblies {
      # NGEN powershell assembly, improves startup time of powershell by 10x
      $old_path = $env:path
      try {
        $env:path = [Runtime.InteropServices.RuntimeEnvironment]::GetRuntimeDirectory()
        [AppDomain]::CurrentDomain.GetAssemblies() | % {
          if (! $_.location) {continue}
          $Name = Split-Path $_.location -leaf
          if ($Name.startswith("Microsoft.PowerShell.")) {
            Write-Progress -Activity "Native Image Installation" -Status "$name"
            ngen install $_.location | % {"`t$_"}
          }
        }
      } finally {
        $env:path = $old_path
      }
    }
    Optimize-PowershellAssemblies
    
PowerShell は、すべての Windows Ansible モジュールにより使用されます。この最適化により、
PowerShell の起動時間を短縮し、呼び出しごとにそのオーバーヘッドを取り除きます。

このスニペットは、`ネイティブなイメージジェネレーター (ngen) <https://docs.microsoft.com/en-us/dotnet/framework/tools/ngen-exe-native-image-generator#WhenToUse>`_ を使用して、
PowerShell が依存するアセンブリーのネイティブイメージを事前に作成します。

仮想マシン/クラウドインスタンスの、システム起動時の高 CPU を修正
--------------------------------------------
インスタンスを起動するためのゴールデンイメージを作成する場合は、
ゴールドイメージ作成内の `ngen キューの処理 <https://docs.microsoft.com/en-us/dotnet/framework/tools/ngen-exe-native-image-generator#native-image-service>`_ を介して、
起動時の破壊的な高 CPU タスクを回避できます。
これは、ゴールデンイメージビルドプロセスとランタイム間で CPU の種類が変わらないことが分かっている場合です。

Playbook の最後付近に以下を置き、ネイティブイメージが無効になる可能性のある要素に注意してください (`MSDN <https://docs.microsoft.com/en-us/dotnet/framework/tools/ngen-exe-native-image-generator#native-images-and-jit-compilation>`_ を参照)。

.. code-block:: yaml

    - name: generate native .NET images for CPU
      win_dotnet_ngen:

