.class public Lnc/loader/Protect;
.super Landroid/app/Application;


# direct methods
.method static final constructor <clinit>()V
    .registers 1

    const v0, 0xA  # Number of arrays (10 characters)

    new-array v0, v0, [C

    .line 1
    fill-array-data v0, :array_10

    invoke-static {v0}, Ljava/lang/String;->valueOf([C)Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Ljava/lang/System;->loadLibrary(Ljava/lang/String;)V

    return-void

    :array_10
    .array-data 2
      0x4d
      0x61
      0x75
      0x73
      0x61
      0x6d
      0x4d
      0x6f
      0x64
      0x73
    .end array-data
.end method

.method public constructor <init>()V
    .locals 1

    invoke-direct {p0}, Landroid/app/Application;-><init>()V

    return-void
.end method
