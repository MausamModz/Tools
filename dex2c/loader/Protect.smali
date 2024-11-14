.class public Lnp/loader/Protect;
.super Landroid/app/Application;


# direct methods
.method static final constructor <clinit>()V
    .registers 1

    const v0, 0x5

    new-array v0, v0, [C

    .line 1
    fill-array-data v0, :array_10

    invoke-static {v0}, Ljava/lang/String;->valueOf([C)Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Ljava/lang/System;->loadLibrary(Ljava/lang/String;)V

    return-void

    :array_10
    .array-data 2
        0x64
        0x65
        0x78
        0x32
        0x63
    .end array-data
.end method

.method public native constructor <init>()V
.end method

.method public static final native initDcc()V
.end method


