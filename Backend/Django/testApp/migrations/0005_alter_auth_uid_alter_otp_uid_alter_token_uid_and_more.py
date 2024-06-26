# Generated by Django 5.0.6 on 2024-06-02 17:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "testApp",
            "0004_rename_created_token_creation_date_remove_token_user_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="auth",
            name="uid",
            field=models.ForeignKey(
                db_column="uid",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="auth",
                to="testApp.user",
            ),
        ),
        migrations.AlterField(
            model_name="otp",
            name="uid",
            field=models.ForeignKey(
                db_column="uid",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="otp",
                to="testApp.user",
            ),
        ),
        migrations.AlterField(
            model_name="token",
            name="uid",
            field=models.ForeignKey(
                db_column="uid",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="token",
                to="testApp.user",
            ),
        ),
        migrations.AlterModelTable(
            name="auth",
            table="auth",
        ),
        migrations.AlterModelTable(
            name="otp",
            table="otp",
        ),
        migrations.AlterModelTable(
            name="token",
            table="tokens",
        ),
        migrations.AlterModelTable(
            name="user",
            table="users",
        ),
    ]
