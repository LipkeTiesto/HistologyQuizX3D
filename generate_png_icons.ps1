Add-Type -AssemblyName System.Drawing

function Generate-PwaIcon {
    param(
        [int]$Size,
        [string]$OutputPath
    )

    $bmp = New-Object System.Drawing.Bitmap $Size, $Size
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $g.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality

    # Background squircle
    $rect = New-Object System.Drawing.Rectangle 0, 0, $Size, $Size
    $bgBrush = New-Object System.Drawing.Drawing2D.LinearGradientBrush(
        (New-Object System.Drawing.Point 0, 0),
        (New-Object System.Drawing.Point $Size, $Size),
        [System.Drawing.Color]::FromArgb(15, 23, 42),
        [System.Drawing.Color]::FromArgb(2, 6, 23)
    )
    $g.FillRectangle($bgBrush, $rect)

    # Scale factor
    $scale = $Size / 512.0
    $cx = $Size / 2.0
    $cy = $Size / 2.0

    # Concentric rings
    $ringPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(50, 59, 130, 246), (1.5 * $scale))
    $g.DrawEllipse($ringPen, ($cx - 180 * $scale), ($cy - 180 * $scale), (360 * $scale), (360 * $scale))
    $g.DrawEllipse($ringPen, ($cx - 140 * $scale), ($cy - 140 * $scale), (280 * $scale), (280 * $scale))

    # Outer lens bezel with gradient
    $bezelPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(255, 6, 182, 212), (7 * $scale))
    $g.DrawEllipse($bezelPen, ($cx - 116 * $scale), ($cy - 116 * $scale), (232 * $scale), (232 * $scale))

    # Target crosshair ticks
    $tickPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(255, 56, 189, 248), (5 * $scale))
    $tickPen.StartCap = [System.Drawing.Drawing2D.LineCap]::Round
    $tickPen.EndCap = [System.Drawing.Drawing2D.LineCap]::Round
    $g.DrawLine($tickPen, [float]$cx, [float]($cy - 134 * $scale), [float]$cx, [float]($cy - 114 * $scale))
    $g.DrawLine($tickPen, [float]$cx, [float]($cy + 114 * $scale), [float]$cx, [float]($cy + 134 * $scale))
    $g.DrawLine($tickPen, [float]($cx - 134 * $scale), [float]$cy, [float]($cx - 114 * $scale), [float]$cy)
    $g.DrawLine($tickPen, [float]($cx + 114 * $scale), [float]$cy, [float]($cx + 134 * $scale), [float]$cy)

    # Central cell polygon (Hexagon)
    $hexPoints = @(
        (New-Object System.Drawing.PointF ($cx + 0), ($cy - 46 * $scale)),
        (New-Object System.Drawing.PointF ($cx + 40 * $scale), ($cy - 23 * $scale)),
        (New-Object System.Drawing.PointF ($cx + 40 * $scale), ($cy + 23 * $scale)),
        (New-Object System.Drawing.PointF ($cx + 0), ($cy + 46 * $scale)),
        (New-Object System.Drawing.PointF ($cx - 40 * $scale), ($cy + 23 * $scale)),
        (New-Object System.Drawing.PointF ($cx - 40 * $scale), ($cy - 23 * $scale))
    )
    $hexFill = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(60, 14, 165, 233))
    $hexStroke = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(255, 99, 102, 241), (3.5 * $scale))
    $g.FillPolygon($hexFill, $hexPoints)
    $g.DrawPolygon($hexStroke, $hexPoints)

    # Core Nucleus
    $nucGlow = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(180, 6, 182, 212))
    $g.FillEllipse($nucGlow, ($cx - 16 * $scale), ($cy - 16 * $scale), (32 * $scale), (32 * $scale))
    $nucCore = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::White)
    $g.FillEllipse($nucCore, ($cx - 10 * $scale), ($cy - 10 * $scale), (20 * $scale), (20 * $scale))

    # Save
    $bmp.Save($OutputPath, [System.Drawing.Imaging.ImageFormat]::Png)
    $g.Dispose()
    $bmp.Dispose()
    Write-Host "Generated: $OutputPath ($Size x $Size)"
}

Generate-PwaIcon -Size 192 -OutputPath "icon-192.png"
Generate-PwaIcon -Size 512 -OutputPath "icon-512.png"
Generate-PwaIcon -Size 180 -OutputPath "apple-touch-icon.png"
Generate-PwaIcon -Size 32 -OutputPath "favicon-32.png"
