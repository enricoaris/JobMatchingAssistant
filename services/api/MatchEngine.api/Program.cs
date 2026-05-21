using MatchEngine.Api.Consumer;
using MatchEngine.Api.Helper;
using MatchEngine.Api.Hubs;
using MatchEngine.Api.Processor;
using MatchEngine.Api.Workers;
using Microsoft.EntityFrameworkCore;
using Npgsql;
using Resume.Shared.Data;
using Resume.Shared.Messaging;

var builder = WebApplication.CreateBuilder(args);

var connectionString = builder.Configuration.GetConnectionString("DefaultConnection");

// Add services to the container.

builder.Services.AddControllers();
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseNpgsql(connectionString, x => x.UseVector()));
builder.Services.AddSingleton<RabbitMqPublisher>();

builder.Services.AddScoped<JobHelper>();
builder.Services.AddScoped<ResumeHelper>();
builder.Services.AddScoped<MatchHelper>();
builder.Services.AddScoped<PdfHelper>();

builder.Services.AddScoped<StatusUpdateProcessor>();
builder.Services.AddScoped<MatchingProcessor>();
builder.Services.AddScoped<ResumeProcessor>();

builder.Services.AddSingleton<JobStatusUpdateConsumer>();
builder.Services.AddSingleton<ResumeStatusUpdateConsumer>();
builder.Services.AddSingleton<ResumeEmbeddedConsumer>();
builder.Services.AddSingleton<ResumeUploadedConsumer>();

builder.Services.AddHostedService<JobStatusUpdateWorker>();
builder.Services.AddHostedService<ResumeStatusUpdateWorker>();
builder.Services.AddHostedService<MatchingWorker>();
builder.Services.AddHostedService<ResumeTextWorker>();

builder.Services.AddNpgsqlDataSource(connectionString, dataSourceBuilder => {
    dataSourceBuilder.UseVector();
    dataSourceBuilder.EnableDynamicJson();
});

builder.Services.AddDbContext<AppDbContext>((sp, options) => {
    options.UseNpgsql(sp.GetRequiredService<NpgsqlDataSource>());
});

builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowFrontend",
        policy => policy
        .WithOrigins("http://localhost:5173")
        .AllowAnyHeader()
        .AllowAnyMethod()
        .AllowCredentials());
});

builder.Services.AddSignalR();

var app = builder.Build();

app.MapHub<ProcessingHub>("/hubs/processing");

// Configure the HTTP request pipeline.
app.UseCors("AllowFrontend");

app.UseHttpsRedirection();

app.UseAuthorization();

app.MapControllers();

app.Run();
